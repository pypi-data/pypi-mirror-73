from sqlpie.model_engine import ModelEngine
from sqlpie.project import Project
from sqlpie.exceptions import BadInputError
import dag

class Sqlpie:
	#render single model
	#Sqlpie(model = 'model_1')
	#render single model with payload
	#Sqlpie(model = 'model_1', vars_payload={'key': 'value'}) 
	#render multiple selected models
	#Sqlpie(models = ['model_1', 'model_2']) 
	#render multiple selected models with payload
	#Sqlpie(models = ['model_1', 'model_2'], {'model_1': {'key': 'value'}})
	#render all but model that are passed in the excludes params
	#Sqlpie(excludes = ['model_3', model_4])
	#render all but model that are passed in the excludes params with payloads
	#Sqlpie(excludes = ['model_3', model_4], vars_payload={'model_1': {'key': value}}) 
	#render all models
	#Sqlpie()
	#render all models with payload
	#Sqlpie(vars_payload={'model_1': {'key':'value'}, 'model_2': { 'key': 'value' }})
	def __init__(self, **kwargs):
		self.models = {}
		self.api_data = {}
		conf_keys = list(kwargs.keys())
		conf_keys.sort()
		if not kwargs:
			self.render_all()
		elif conf_keys == ['vars_payload']:
			self.render_all(vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['model']:
			self.render_single(model=kwargs['model'])
		elif conf_keys == ['model', 'vars_payload']:
			self.render_single(model=kwargs['model'], vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['models']:
			self.render_multiple(models=kwargs['models'])
		elif conf_keys == ['models', 'vars_payload']:
			self.render_multiple(models=kwargs['models'], vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['excludes']:
			self.exclude_and_render(excludes=kwargs['excludes'])
		elif conf_keys.sort() == ['excludes', 'vars_payload']:
			self.exclude_and_render(excludes=kwargs['excludes'], vars_payload=kwargs['vars_payload'])
		else:
			raise BadInputError

	def render_all(self, vars_payload={}):
		all_models = Project.models()
		self.render_multiple(all_models, vars_payload)

	def exclude_and_render(self, excludes, vars_payload={}):
		all_models = Project.models()
		models_after_exclusion = [i for i in all_models if not i in excludes]
		self.render_multiple(models=models_after_exclusion, vars_payload=vars_payload)

	def render_multiple(self, models, vars_payload={}):
		for model in models:
			if model in vars_payload.keys():
				self.render_single(model, vars_payload[model])
			else:
				self.render_single(model)

	def render_single(self, model, vars_payload={}):
		model = ModelEngine(model, vars_payload)
		self.models[model.model] = model
		self.api_data[model.model] = self.build_model_api_data(model)

	def build_model_api_data(self, model):
		return 	{
							'rendered_model': model.rendered_model,
							'viz_data': model.viz_data_prep(),
							'ind_nodes': model.dag.ind_nodes(),
							'all_leaves': model.dag.all_leaves(),
							'graph_object': self.parse_graph_object(model.dag.graph),
							'dag_topological_sort': model.dag.topological_sort(),
							'dag_itterable_object': self.dag_itterable_object(model.dag)
						}

	def dag_itterable_object(self, dag):
		obj = {}
		for node in dag.topological_sort():
			obj[node] = {'predecessors': dag.predecessors(node), 'downstreams': dag.downstream(node) }
		return obj

	def parse_graph_object(self, graph):
		dict_graph = dict(graph)
		for key in dict_graph.keys():
			dict_graph[key] = list(dict_graph[key])
		return dict_graph
