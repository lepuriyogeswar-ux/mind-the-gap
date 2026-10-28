from app.simulator import demo_graph, simulate

def test_demo_graph_has_edges_and_nodes():
 graph=demo_graph(); assert len(graph['nodes'])>=5; assert len(graph['edges'])>=5

def test_database_failure_includes_dependents():
 result=simulate('database_down'); assert result['target']=='database'; assert 'api' in result['predicted_affected']; assert 'auth' in result['predicted_affected']; assert result['is_live_experiment'] is False

def test_model_api_failure_has_mitigation():
 result=simulate('model_api_down'); assert 'api' in result['predicted_affected']; assert result['recommendations']; assert result['caveat']

def test_config_scenario_is_available():
 assert simulate('config_missing')['target']=='config'

def test_unknown_scenario_rejected():
 try: simulate('not-a-scenario')
 except ValueError: pass
 else: raise AssertionError('Unknown scenario should raise ValueError')
