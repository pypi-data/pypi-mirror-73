#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json

# Classes: CamelCase
# Variables & arguments: low_case_underscores


# # PathManager
# `PathManager` is an efficient, easy and convenient way to manage and access your local paths in python.
# 
# 1. All your paths and shortcuts are saved locally in a `paths.json` file.
# 2. Set custom paths by `paths.set(...)` and get custom paths by `paths.get(...)` or `paths[...]` or `paths.{...}`.
# 3. Create shortcuts to subdirectories by `paths[...].set_shortcut(...)` and access it by `paths[...].shortcut(...)` or `paths[... , ...]`.
# 
# ---
# 
# ## Example
# In this example we'll see how to save the path to your "datasets" folder and how to define a shortcut to a "dogs" subdirectory in the "datasets" folder.
# 
# ### Save a path to your datasets folder
# You can save the path to your datasets folder with the following code: `paths['datasets'] = 'desktop/projects/datasets'`,
# 
# and if we would to print it using `print(paths['datasets'])` we would get: `'desktop/projects/datasets'`.
# 
# 
# ### Create a shortcut to a subdirectory or subfile in that folder
# You can create a shortcut to a "dogs" subdirectory of the original path with the following code: 
# `paths['datasets', 'dogs'] = 'animals/dogs'`,
# 
# and if we would to print it we using `print(paths['datasets', 'dogs'])` would get `'desktop/projects/datasets/animals/dogs'`.
# 
# 
# ---
# 
# ## paths.json
# The `paths.json` file contains all of the custom paths and shortcuts that you create, by default the file is saved at `...` but this can be changed to a custom path if needed.
# 
# The file is constructed in the following structure:
# 
# <code>[
#     {
#         NAME: "...",
#         PATH: "...",
#         SHORTCUTS: [{ NAME: "...", SUBPATH: "..." }]
#     }
# ]</code>
# 
# ---
# 
# ## `add` vs `set`
# ### The `set` function
# Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, if it exists in the manager then the current path for that name is replaced with the new one.
# 
# ### The `add` function
# Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, raising a `PathNameDuplicate` error if the path's name already exists in the manager (to override see the `set` function).
# 
# ---
# 
# ### The `get` function
# Retrive a path from the `paths.json` file, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.
# 
# Examples:
# - By function: `mypath = paths.get(name)`.
# - By index: `mypath = paths[name]` (Invokes the 'get' function).
# - By property: `mypath = paths.name` (Invokes the 'get' function).
# 
# ---
# 
# ### The `delete` function
# Delete a path from the `paths.json` file only if the file exists in the manager, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.
# 
# Examples:
# - `paths.delete(name)`.
# - `paths.get(name).delete()`.
# 
# Note: The `get` function can also be invoked by index or property like before (i.e `paths[name].delete()` or `paths.name.delete()`)
# 
# ---
# 
# ## `add_shortcut` vs `set_shortcut`
# Assign a shortcut to easily access a subdirectory or subfile within a specific path.
# 
# ### The `set_shortcut` function
# Add a new shortcut to easily access a subdirectory or subfile within a path, shortcut is added only if the shortcut's name doesn't exist in the current path's shortcuts, if it does exist then the path for that shortcut's name is replaced with the new one.
# 
# ### The `add_shortcut` function
# Add a new shortcut to easily access a subdirectory or subfile within a path, raising a `ShortcutNameDuplicate` error if the shortcut's name already exists in the current path's shortcuts.
# 
# --- 
# 
# ### The `delete_shortcut` function
# Delete a shortcut from the path's shortcuts.
# 
# ---
# 
# ### The `shortcuts` function
# Retrive all shortcuts of the current path's shortcuts.
# 
# ---
# 
# ### The `shortcut` function
# Retrive a shortcut from the current path's shortcuts.

# In[2]:


DEFAULT_JSON_PATH = os.getcwd() + '/paths.json'

class ShortcutObject:
    def __init__(self, path_obj, name, subpath):
        self.name = name
        self.subpath = subpath
        self.path_obj = path_obj
        
    def delete(self):
        """
        Delete the current shortcut from the path object.
        """
        return self.path_obj.delete_shortcut(self.name)
    
    @property
    def fullpath(self):
        """
        Concatenate the path of the path object with the subpath of this shortcut, i.e. get the full path of the shortcut.
        """
        return os.path.join(self.path_obj.path, self.subpath)
    
    def __repr__(self):
         return self.fullpath
    def __str__(self):
        return self.fullpath


# In[3]:


class PathObject(json.JSONEncoder):
    def __init__(self, manager, name, path):
        self.name = name
        self.path = path
        self.manager = manager
        self.shortcuts = {}
        
    def delete(self):
        """
        Delete the current path from the manager.
        """
        return self.manager.delete(self.name)
        
    def add_shortcut(self, name, subpath):
        """
        Add a new shortcut to easily access a subdirectory or subfile within a path, raising a `ShortcutNameDuplicate` error if the shortcut's name already exists in the current path's shortcuts.
        
        Parameters:
            name: The name of the shortcut.
            path: A relative path for a subdirectory or subfile. (for example, in a `datasets` path you can have `dogs/cute_dogs`).
        """
        if name in self.shortcuts:
            raise Exception('ShortcutNameDuplicate: `{}` is already in `{}` shortcuts.'.format(name, self.name))
        
        self.shortcuts[name] = ShortcutObject(self, name, subpath)
        self.manager.save_json()

    def set_shortcut(self, name, subpath):
        """
        Add a new shortcut to easily access a subdirectory or subfile within a path, shortcut is added only if the shortcut's name doesn't exist in the current path's shortcuts, if it does exist then the path for that shortcut's name is replaced with the new one.
        
        Parameters:
            name: The name of the shortcut.
            path: A relative path for a subdirectory or subfile. (for example, in a `datasets` path you can have `dogs/cute_dogs`).
        """
        self.shortcuts[name] = ShortcutObject(self, name, subpath)
        self.manager.save_json()

    def get_shortcut(self, name):
        """
        retrive a shortcut from the current path's shortcuts.
        
        Parameters:
            name: The name of the shortcut.
        """
        if name not in self.shortcuts:
            raise Exception('ShotcutNameNotFound: `{}` was not found in `{}` shortcuts.'.format(name, self.name))
        return self.shortcuts[name]
    
    def shortcut(self, name):
        """
        Same as `paths.get_shortcut`, retrive a shortcut from the current path's shortcuts.

        Parameters:
            name: The name of the shortcut.
        """
        return self.get_shortcut(name)
    
    def delete_shortcut(self, name):
        """
        Delete a shortcut from the path's shortcuts.
        
        Parameters:
            name: The name of the shortcut.
        """
        if name not in self.shortcuts:
            raise Exception('ShotcutNameNotFound: `{}` was not found in `{}` shortcuts.'.format(name, self.name))
        del self.shortcuts[name]
        self.manager.save_json()
        
    def __getitem__(self, shortcut_name):
        return self.get_shortcut(shortcut_name)
        
    def __setitem__(self, shortcut_name, shortcut_subpath):
        self.set_shortcut(shortcut_name, shortcut_subpath)
        
    def __repr__(self):
         return self.path
    def __str__(self):
        return self.path


# In[4]:


class PathManager:
    def __init__(self, json_path=None):
        self.json_path = json_path if json_path else DEFAULT_JSON_PATH
        
        if os.path.exists(self.json_path):
            self.load_json()
        else:
            self.paths = {}
    
    def add(self, name, path):
        """
        Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, raising a `PathNameDuplicate` error if the path's name already exists in the manager (to override see the `set` function).

        Parameters:
            name: The name of the path (for example `datasets`).
            path: A path to a directory or file.
        """
        if name in self.paths:
            raise Exception('PathNameDuplicate: `{}` is already in the path manager.'.format(name))
        
        self.paths[name] = PathObject(self, name, path)
        self.save_json()
        
    def set(self, name, path):
        """
        Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, if it exists in the manager then the current path for that name is replaced with the new one.
        
        Parameters:
            name: The name of the path (for example `datasets`).
            path: A path to a directory or file.
        """
        self.paths[name] = PathObject(self, name, path)
        self.save_json()
        
    def get(self, name):
        """
        Retrive a path from the `paths.json` file, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.
        
        Parameters:
            name: The name of the path (for example `datasets`).
        
        Examples:
            - By function: `mypath = paths.get(name)`.
            - By index: `mypath = paths[name]` (Invokes the 'get' function).
            - By property: `mypath = paths.name` (Invokes the 'get' function).
        """
        if name not in self.paths:
            raise Exception('PathNameNotFound: `{}` was not found in the path manager.'.format(name))
            
        return self.paths[name]
    
    def delete(self, name):
        """
        Delete a path from the `paths.json` file only if the file exists in the manager, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.

        Parameters:
            name: The name of the path (for example `datasets`).

        Examples:
            - `paths.delete(name)`.
            - `paths.get(name).delete()`.

        Note: The `get` function can also be invoked by index or property like before (i.e `paths[name].delete()` or `paths.name.delete()`)
        """
        if name not in self.paths:
            raise Exception('PathNameNotFound: `{}` was not found in the path manager.'.format(name))
        del self.paths[name]
        self.save_json()
        
    def __getitem__(self, args):
        if not isinstance(args, tuple):
            name = args
            return self.get(name)
        elif len(args) == 2:
            name = args[0]
            shortcut_name = args[1]
            return self.get(name).shortcut(shortcut_name)
        
    def __setitem__(self, *args):
        if isinstance(args[0], tuple):
            name = args[0][0]
            shortcut_name = args[0][1]
            shortcut_subpath = args[1]
            self.get(name).set_shortcut(shortcut_name, shortcut_subpath)
        else:
            name = args[0]
            path = args[1]
            self.set(name, path)
    
    def save_json(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.paths, f, cls=PathAndShortcutEncoder, indent=4)
    
    def load_json(self):
        with open(self.json_path, 'r') as f:
            json_obj = json.load(f)
            
        self.paths = {}
        
        for name in json_obj:
            self.set(name, json_obj[name]['path'])
            name_obj = self.get(name)
            
            for shortcut_name in json_obj[name]['shortcuts']:
                name_obj.set_shortcut(shortcut_name, json_obj[name]['shortcuts'][shortcut_name])


# In[5]:


class PathAndShortcutEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PathObject):
            return { 'path': obj.path, 'shortcuts': obj.shortcuts }
        elif isinstance(obj, ShortcutObject):
            return obj.subpath
        else:
            return super().default(obj)


# In[8]:


paths = PathManager()


# In[ ]:





# In[ ]:





# In[ ]:




