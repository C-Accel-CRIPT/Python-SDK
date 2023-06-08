import weakref

# Store all nodes by their uid and or uuid.
# This way if we load nodes with a know uid or uuid, we take them from the cache instead of instantiating them again.
_node_cache = weakref.WeakValueDictionary()
