# PathManager
`PathManager` is an efficient, easy and convenient way to manage and access your local paths in python.

1. All your paths and shortcuts are saved locally in a `paths.json` file.
2. Set custom paths by `paths.set(...)` and get custom paths by `paths.get(...)` or `paths[...]` or `paths.{...}`.
3. Create shortcuts to subdirectories by `paths[...].set_shortcut(...)` and access it by `paths[...].shortcut(...)` or `paths[... , ...]`.

---

## Example
In this example we'll see how to save the path to your "datasets" folder and how to define a shortcut to a "dogs" subdirectory in the "datasets" folder.

### Save a path to your datasets folder
You can save the path to your datasets folder with the following code: `paths['datasets'] = 'desktop/projects/datasets'`,

and if we would to print it using `print(paths['datasets'])` we would get: `'desktop/projects/datasets'`.


### Create a shortcut to a subdirectory or subfile in that folder
You can create a shortcut to a "dogs" subdirectory of the original path with the following code: 
`paths['datasets', 'dogs'] = 'animals/dogs'`,

and if we would to print it we using `print(paths['datasets', 'dogs'])` would get `'desktop/projects/datasets/animals/dogs'`.


---

## paths.json
The `paths.json` file contains all of the custom paths and shortcuts that you create, by default the file is saved at `...` but this can be changed to a custom path if needed.

The file is constructed in the following structure:

<code>[
    {
        NAME: "...",
        PATH: "...",
        SHORTCUTS: [{ NAME: "...", SUBPATH: "..." }]
    }
]</code>

---

## `add` vs `set`
### The `set` function
Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, if it exists in the manager then the current path for that name is replaced with the new one.

### The `add` function
Add a new path to the `paths.json` file only if the path's name doesn't exist in the manager, raising a `PathNameDuplicate` error if the path's name already exists in the manager (to override see the `set` function).

---

### The `get` function
Retrive a path from the `paths.json` file, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.

Examples:
- By function: `mypath = paths.get(name)`.
- By index: `mypath = paths[name]` (Invokes the 'get' function).
- By property: `mypath = paths.name` (Invokes the 'get' function).

---

### The `delete` function
Delete a path from the `paths.json` file only if the file exists in the manager, raising a `PathNameNotFound` error if the path's name doesn't exist in the manager.

Examples:
- `paths.delete(name)`.
- `paths.get(name).delete()`.

Note: The `get` function can also be invoked by index or property like before (i.e `paths[name].delete()` or `paths.name.delete()`)

---

## `add_shortcut` vs `set_shortcut`
Assign a shortcut to easily access a subdirectory or subfile within a specific path.

### The `set_shortcut` function
Add a new shortcut to easily access a subdirectory or subfile within a path, shortcut is added only if the shortcut's name doesn't exist in the current path's shortcuts, if it does exist then the path for that shortcut's name is replaced with the new one.

### The `add_shortcut` function
Add a new shortcut to easily access a subdirectory or subfile within a path, raising a `ShortcutNameDuplicate` error if the shortcut's name already exists in the current path's shortcuts.

--- 

### The `delete_shortcut` function
Delete a shortcut from the path's shortcuts.

---

### The `shortcuts` function
Retrive all shortcuts of the current path's shortcuts.

---

### The `shortcut` function
Retrive a shortcut from the current path's shortcuts.
