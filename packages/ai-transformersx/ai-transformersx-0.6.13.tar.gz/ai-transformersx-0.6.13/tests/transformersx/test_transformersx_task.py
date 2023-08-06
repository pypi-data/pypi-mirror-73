from transformers import BertModel

from transformersx.data import TaskDataProcessor
from transformersx.task import DefaultTransformerTask, TaskConfig
from transformersx.train import TaskContext


class DefaultTransformerTaskForTest(DefaultTransformerTask):
    def __init__(self, config: TaskConfig):
        super().__init__(config)

    def _create_task_context(self, config: TaskConfig) -> TaskContext:
        data_processor = TaskDataProcessor()
        data_processor.get_labels = lambda: ['0']
        return TaskContext(
            task_name='sentiment',
            data_processor=data_processor,
            model_class=BertModel,
            compute_metrics=self.compute_metrics
        )

    def compute_metrics(self):
        pass


class Test_Transformersx_task:
    def test_default_task(self):
        DefaultTransformerTaskForTest(TaskConfig())
