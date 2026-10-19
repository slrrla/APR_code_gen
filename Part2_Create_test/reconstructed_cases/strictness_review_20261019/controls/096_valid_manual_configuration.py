from pathlib import Path
home = Path.home()
settings = home / '.qiskit' / 'settings.conf'
kernel = home / '.ipython' / 'profile_default' / 'ipython_kernel_config.py'
settings.parent.mkdir(parents=True, exist_ok=True)
kernel.parent.mkdir(parents=True, exist_ok=True)
if not settings.exists():
    settings.write_text('[default]\ncircuit_drawer = text\n', encoding='utf-8')
if not kernel.exists():
    kernel.write_text('# Manual kernel configuration\n', encoding='utf-8')
