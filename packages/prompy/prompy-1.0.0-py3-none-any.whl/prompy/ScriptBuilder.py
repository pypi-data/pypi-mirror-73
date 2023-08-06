import nbimporter
import importlib
import textwrap
import os

from prom4py.ProcessDiscovery import *


def to_java_array(pythonList, array_variable_name):
    if len(pythonList) == 0:
        return ''
    if type(pythonList[0]).__name__ == 'str':
        return f'String[] {array_variable_name} = {{' + '"'.join(str(pythonList)[1:-1].split("'")) + '};'
    elif type(pythonList[0]).__name__ == 'int':
        return f'Integer[] {array_variable_name} = {{{str(pythonList)[1:-1]}}};'
    elif type(pythonList[0]).__name__ == 'float':
        return f'Double[] {array_variable_name} = {{{str(pythonList)[1:-1]}}};'
    else:
        raise ValueError(f'{type(pythonList[0]).__name__} type not supported.')


def visualize(j_component_variable_name, height, width, filename=''):
    if filename == '':
        filename = f'{os.getcwd()}/temp.png'
    return f'''
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
JFrame frame = new JFrame();
frame.add({j_component_variable_name});
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.setSize({height}, {width});
frame.setVisible(true);
BufferedImage image = new BufferedImage(500, 500, 1);
Graphics2D graphics2D = image.createGraphics();
frame.paint(graphics2D);
ImageIO.write(image, "png", new File("{filename}"));
'''


def end():
    return 'print("Done, exiting.");exit();'


def show_script(script_string):
    script = textwrap.dedent(';\n'.join(script_string.split(';')))
    lines = script.split('\n')
    return '\n'.join([f'{i + 1:>3}: {line}' for i, line in enumerate(lines)])


def get_petrinet(petrinet_filename, from_variable=False, variable_prefix=''):
    if from_variable:
        script_string = f'\n_petrinetImportResult = import_petri_net_from_pnml_file({petrinet_filename});'
    else:
        script_string = f'\n_petrinetImportResult = import_petri_net_from_pnml_file("{petrinet_filename}");'
    script_string += f'\n{variable_prefix}petrinet = _petrinetImportResult[0];'
    script_string += f'\n{variable_prefix}marking = _petrinetImportResult[1];'
    return script_string


def get_log(log_filename, from_variable=False, variable_prefix=''):
    if from_variable:
      return f'{variable_prefix}log = open_xes_log_file({log_filename});'
    else:
      return f'{variable_prefix}log = open_xes_log_file("{log_filename}");'


def get_mapping(net_variable_name, log_variable_name, classifier='default', variable_prefix='', help=False):
    if help:
        print('hallo')
    imports = 'import org.processmining.plugins.connectionfactories.logpetrinet.TransEvClassMapping;'
    imports += '\nimport org.processmining.pnetreplayer.utils.TransEvClassMappingUtils;'
    imports += '\nimport org.processmining.log.utils.XUtils;'
    imports += '\nimport org.deckfour.xes.classification.XEventClasses;'
    imports += '\nimport org.deckfour.xes.classification.XEventClassifier;'
    imports += '\nimport org.deckfour.xes.classification.XEventNameClassifier;'
    if classifier == 'default':
        classifier = f'XEventClassifier {variable_prefix}classifier = XUtils.getDefaultClassifier({log_variable_name});'
    elif classifier is 'eventname':
        classifier = 'XEventClassifier {variable_prefix}classifier = new XEventNameClassifier();'
    else:
        raise NotImplementedError()
    event_classes = f'{variable_prefix}eventClasses = XEventClasses.deriveEventClasses({variable_prefix}classifier, {log_variable_name}).getClasses();\nSet activities = new HashSet({variable_prefix}eventClasses);'
    mapping = f'{variable_prefix}mapping = TransEvClassMappingUtils.getInstance().getMapping({net_variable_name}, activities, classifier);'
    return  '\n'.join([imports, classifier, event_classes, mapping])


def get_fitness(net_variable_name, log_variable_name, mapping_variable_name, event_classes_variable_name='eventClasses',
                parameter_variable_name=None, variable_prefix=''):
    imports = 'import org.processmining.plugins.astar.petrinet.PetrinetReplayerWithoutILP;'
    algorithm = f'{variable_prefix}algorithm = new PetrinetReplayerWithoutILP();'
    parameters = ''
    if parameter_variable_name is None:
        parameters = 'import org.processmining.plugins.petrinet.replayer.algorithms.costbasedcomplete.CostBasedCompleteParam;'
        parameters += f'{variable_prefix}parameters = new CostBasedCompleteParam({event_classes_variable_name}, {mapping_variable_name}.getDummyEventClass(), {net_variable_name}.getTransitions());'
    result = f'{variable_prefix}result = replay_a_log_on_petri_net_for_conformance_analysis({net_variable_name}, {log_variable_name}, {mapping_variable_name}, {variable_prefix}algorithm, {variable_prefix}parameters);'
    return  '\n'.join([imports, algorithm, parameters, result])


def get_precision(net_variable_name, marking_variable_name, mapping_variable_name=None, alignment_result_variable_name=None,
                  strategy='precgen', variable_prefix=''):
    if strategy == 'precgen':
        if mapping_variable_name is None:
            raise ValueError('mapping_variable_name missing.')
        script = 'import org.processmining.plugins.pnalignanalysis.conformance.AlignmentPrecGen;';
        script += f'\nAlignmentPrecGen {variable_prefix}precGeneralization = new AlignmentPrecGen();'
        script += f'\n{variable_prefix}result = {variable_prefix}precGeneralization.measureConformanceAssumingCorrectAlignment(null, {mapping_variable_name}, {alignment_result_variable_name}, {net_variable_name}, {marking_variable_name}, false);'
    elif strategy == 'eigenvalue_based':
        script = f'{variable_prefix}result = eigenvalue_based_precision_petrinet_({log_variable_name}, {net_variable_name});'
    return script



def get_conformance(net_variable_name, marking_variable_name, log_variable_name, classifier='default', precision_strategy='precgen', variable_prefix=''):
    script = get_mapping(net_variable_name, log_variable_name, classifier, variable_prefix)
    script += get_fitness(net_variable_name, log_variable_name,  f'{variable_prefix}mapping', variable_prefix=f'{variable_prefix}_fitness_')
    script += get_precision(net_variable_name, marking_variable_name,  f'{variable_prefix}mapping',
                           alignment_result_variable_name=f'{variable_prefix}_fitness_result',
                           strategy=precision_strategy,
                           variable_prefix=f'{variable_prefix}_precision_')
    return script


def get_soundness(net_variable_name, reduce_model=True, variable_prefix=''):
    script = ''
    if reduce_model:
        script += f'reducedModel = reduce_all_transitions_retain_sink_source_places({net_variable_name});'
        woflan_input = 'reducedModel'
    else:
        woflan_input = net_variable_name
    script += f'\nwoflan = analyze_with_woflan({woflan_input});'
    script += f'\n{variable_prefix}soundness = woflan.isSound();'
    return script


def export_petrinet(net_variable_name, filename):
    return f'pnml_export_petri_net_({net_variable_name}, new File("{filename}"));'


def mine(log_filename, algorithm='alpha', settings={}):
    miner = None
    if algorithm == 'alpha':
        miner = Alpha(log_filename, settings)
    elif algorithm == 'heuristics':
        miner = Heuristics(log_filename, settings)
    elif algorithm == 'inductive':
        miner = Inductive(log_filename, settings)
    elif algorithm == 'ILP':
        miner = ILP(log_filename, settings)
    else:
        raise NotImplementedError()
    return miner.to_java()

