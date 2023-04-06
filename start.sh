cd `dirname $0`

python3 -m pip install wget MuyunxiSupports || python -m pip install wget MuyunxiSupports

python3 main.py || python main.py
