rm -rf dist build *egg-info

python3 setup.py sdist bdist_wheel

rm -rf build *egg-info
