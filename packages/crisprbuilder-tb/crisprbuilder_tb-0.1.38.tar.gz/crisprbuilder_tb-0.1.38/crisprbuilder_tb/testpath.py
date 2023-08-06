import os
from pathlib import Path

item = 'coucou'
print(Path(os.path.dirname(__file__),'REP', 'sequences',
                        item).mkdir(exist_ok=True, parents=True))