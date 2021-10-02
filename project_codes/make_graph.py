from pycallgraph import GlobbingFilter
from pycallgraph import Config
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# import your_function
from image_recognition.recognition_program import main_recognition

#config = Config(max_depth=5)
config = Config()

config.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
    'pydevd_tracing.*',
    '_handle_fromlist',
    '_call_with_frames_removed',
    '_pydev_bundle.*',
    'pydevd.*',
    '_find_and_load',
    '<module>',
    '<lambda>',
    'cb',
    '_ModuleLockManger'
])

graphviz = GraphvizOutput(
    output_file='recognition_program.png', font_size=20, group_font_size=24)

if __name__ == "__main__":
    with PyCallGraph(output=graphviz, config=config):
        main_recognition()
