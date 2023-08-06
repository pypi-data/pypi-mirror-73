import zmq
import multiprocessing
from zpipe.worker import Worker
from zpipe.stages.stage import Stage
from zpipe.utils.ztypes import *
from threading import Thread
import os, time


class NonWorkerStage(Stage):
    def __del__(self):
        if self.outlink is not None:
            self.outlink.close()


    def init(self, stage_id=None, stage_cls=None, cls_args=None, stage_type=NOR,
             itypes=[None], otype=None):
        self.stage_id = stage_id

        # Workers
        self.stage_cls = stage_cls()
        self.cls_args = cls_args

        # Stage
        self.context = zmq.Context()
        self.stage_type = stage_type
        self.itypes = itypes; self.otype = otype

        self.outlink_id = None
        self.outlink = None

        self.inlinks = {}
        self.inlink_info = {}
        self.inlink_poller = zmq.Poller()


    def run(self):
        """
        run stage class wint input arguments from inlinks and put the results
        into outlinks
        """
        self.stage_cls.init_class(self.cls_args)
        self.build_outlink()
        self.build_inlinks()

        args = {}
        while not self.exit.is_set():
            # read inlinks
            if self.stage_type is not SRC:
                # inlinks with dependencies (blocking)
                #   - For the inlinks with dependency, recv with blocking
                for inlink, dep_pos_conf in zip(self.inlinks.keys(), self.inlinks.values()):
                    if dep_pos_conf[DEPENDENCY] is True:
                        if self.itypes[dep_pos_conf[POSITION]] is PYOBJ:
                            args[dep_pos_conf[POSITION]] = inlink.recv_pyobj()
                        elif self.itypes[dep_pos_conf[POSITION]] is BYTES:
                            args[dep_pos_conf[POSITION]] = inlink.recv_multipart(copy=False)

                # inlinks without dependencies (nonblocking)
                #   - For the ready inlinks only, recv data
                ready_inlinks = dict(self.inlink_poller.poll(1))
                for inlink, dep_pos_conf in zip(self.inlinks.keys(), self.inlinks.values()):
                    if inlink in ready_inlinks:
                        if self.itypes[dep_pos_conf[POSITION]] is PYOBJ:
                            args[dep_pos_conf[POSITION]] = inlink.recv_pyobj()
                        elif self.itypes[dep_pos_conf[POSITION]] is BYTES:
                            args[dep_pos_conf[POSITION]] = inlink.recv_multipart(copy=False)

            # run class functionality
            #st = time.time()
            result = self.stage_cls.run(args)
            #et = (time.time() - st) * 1000
            #print(f"{self.stage_cls} took: ", et)


            # put the output to outputlinks
            if self.stage_type is not DST:
                if self.otype is PYOBJ:
                    self.outlink.send_pyobj(result)
                elif self.otype is BYTES:
                    self.outlink.send_multipart(result, copy=False)


    def set_outlink(self, pipe_id):
        """
        set outlink port to build the outlink in the subprocess
        """
        self.outlink_id = str(pipe_id) + '_' + str(self.stage_id)


    def build_outlink(self):
        """
        build outlink socket as a publisher in the stage subprocess
        """
        if self.stage_type is not DST:
            self.outlink = self.context.socket(zmq.PUB)
            os.makedirs("/tmp/emar", exist_ok=True)
            self.outlink.bind("ipc:///tmp/emar/" + self.outlink_id)
            print(f"Stage {self.stage_id} build outlink: /tmp/emar/{self.outlink_id}")


    def add_inlink(self, inlink_id, dependency=False, arg_pos=0, conflate=True):
        """
        add inlink dependency to build inlinks in the subprocess
        """
        if self.stage_type is SRC:
            print("src cannot not have inlink")
        else:
            self.inlink_info[inlink_id] = [dependency, arg_pos, conflate]


    def build_inlinks(self):
        """
        build inlink sockets (subscribers) in the stage subprocess
        """
        if self.stage_type is not SRC:
            for inlink_id, dep_pos_conf in zip(self.inlink_info.keys(), self.inlink_info.values()):
                inlink = self.context.socket(zmq.SUB)
                inlink.setsockopt_string(zmq.SUBSCRIBE, '')
                if dep_pos_conf[CONFLATE] is True:
                    inlink.setsockopt(zmq.CONFLATE, 1)

                os.makedirs("/tmp/emar", exist_ok=True)
                inlink.connect("ipc:///tmp/emar/" + inlink_id)
                print(f"Stage {self.stage_id} build inlink: /tmp/emar/{inlink_id}")
                if dep_pos_conf[DEPENDENCY] is False:
                    self.inlink_poller.register(inlink, zmq.POLLIN)
                self.inlinks[inlink] = dep_pos_conf

