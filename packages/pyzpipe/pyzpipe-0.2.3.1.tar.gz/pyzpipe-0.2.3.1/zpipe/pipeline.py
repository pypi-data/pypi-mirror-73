from zpipe.utils.ztypes import *
from zpipe.stages.worker_stage import WorkerStage

class Pipeline():
    def __init__(self, pipe_id):
        self.stages = []
        self.pipe_id = pipe_id
        self.num_stages = 0


    def add_stage(self, stage):
        """
        Arguments
            stage: stage to add
        Return
            num_stages: the number of current stages in this pipeline
        """
        self.num_stages += 1

        # if stage id is not set, set it with num_stages
        if stage.stage_id is None:
            stage.stage_id = self.num_stages

        if stage.stage_type is not DST:
            stage.set_outlink(self.pipe_id)

        if stage.__class__ == WorkerStage:
            stage.worker_cls.make(stage.cls_args, stage.in_queue, stage.out_queue,
                                  stage.worker_num, stage.stage_type)
        self.stages.append(stage)
        return self.num_stages


    def link_stages(self, src, dst, dependency, arg_pos, conflate):
        if src.stage_type is DST:
            print("dst cannot be the source of a linkage")
            return
        if dst.stage_type is SRC:
            print("src cannot be the destination of a linkage")
            return
        if src.otype not in dst.itypes:
            print("dst itypes don't include src otype")
            return

        print("listen to ", src.outlink_id, " by ", dst.stage_type)
        dst.add_inlink(inlink_id=src.outlink_id, dependency=dependency, arg_pos=arg_pos, conflate=conflate)


    def start(self):
        for stage in self.stages:
            stage.start()


    def pause(self):
        for stage in self.stages:
            stage.pause()


    def stop(self):
        for stage in self.stages:
            stage.stop()

    def terminate(self):
        for stage in self.stages:
            stage.terminate()
