def assign_global_to_local(global_to_local):

	r = []
	for v in global_to_local.keys():
		r.append(tf.assign(global_to_local[v],v))
	with tf.control_dependencies(r):
		a = tf.no_op()
	return a


def assign_local_to_global(local_to_global):

	for v in local_to_global.keys():
		r.append(tf.assign(local_to_global[v],v))
	with tf.control_dependencies(r):
		a = tf.no_op()
	return a


def get_variable_by_name(name):

	return [v for v in tf.get_collection('variables') if v.name == name][0]


def get_global_variable_by_name(name):

	
	return [v for v in tf.global_variables() if v.name == name][0]


def create_global_variables(local_optimizer_vars = []):

	local_to_global = {}
	global_to_local = {}
	with tf.device('/job:ps/task:0'):
		for v in tf.local_variables():
			if v not in local_optimizer_vars:
				v_g = tf.get_variable('g/'+v.op.name,
					shape = v.shape,
					dtype = v.dtype,
					trainable=True,
					collections=[tf.GraphKeys.GLOBAL_VARIABLES,
								tf.GraphKeys.TRAINABLE_VARIABLES])
				local_to_global[v] = v_g
				global_to_local[v_g] = v
	return local_to_global,global_to_local


def add_global_variables_to_local_collection():
	r =[]
	for var in tf.get_default_graph()._collections[tf.GraphKeys.GLOBAL_VARIABLES]:
		tf.add_to_collection(tf.GraphKeys.LOCAL_VARIABLES,var)
		r.append(var)
	return r


def clear_global_collection():
	g = tf.get_default_graph()
	for _ in range(len(g._collections[tf.GraphKeys.GLOBAL_VARIABLES])):
		del g._collections[tf.GraphKeys.GLOBAL_VARIABLES][0]
