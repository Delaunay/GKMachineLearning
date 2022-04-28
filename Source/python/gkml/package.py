import os
import glob
import shutil
import json
import re

UnrealEngineRoot = "/media/setepenre/Games/UnrealEngine"
ThirdParty = os.path.join(UnrealEngineRoot, "Engine/Binaries/ThirdParty")
Platform = "Linux"
# Dest = "/media/setepenre/Games/Packaged/Engine/Binaries/Linux"

EngineDir = '/media/setepenre/Games/UnrealEngine/Engine'
Binaries = os.path.join(EngineDir, 'Binaries/Linux')
Target = 'UnrealEditor-Linux-Debug.target'

def package(target):
    """Tries to speedup UE5 loading by creating symlink to shared libraries close to the Editor
    
    Note
    ----
    Unclear if it speeds up anything

    """
    with open(target, 'r') as f:
        target_data = json.load(f)

    dependencies = target_data.get('BuildProducts', [])

    shared = re.compile(r'.*\.so')

    for dep in dependencies:
        path = dep['Path']
        type = dep['Type']

        if shared.match(path):
            name = path.split('/')[-1]
            resolved = path.replace('$(EngineDir)', EngineDir)

            try:
                os.symlink(resolved, os.path.join(Binaries, name)) 
                print('Added a link')
            except FileExistsError:
                print('Skipping')

            print(os.path.join(Binaries, name))
                
            


package(os.path.join(Binaries, Target))

# for a in os.listdir(ThirdParty):
#     Lib =
#     print(a)

# pattern = f"{ThirdParty}/**/Linux/**/*.so"
# files = glob.glob(pattern, recursive=True)


# for file in files:
#     print(file, os.path.join(Dest, file.split("/")[-1]))
#     shutil.copy(file, Dest)


# Get the UnrealEditor-Linux-Debug.target
# and fetch all the files there
