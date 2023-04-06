cd `dirname $0`

if [ python3 ]; then
    alias py='python3'
elif [ python ]; then
    alias py='python'
else
    echo "Please install Python3 to run this script correctly. "
    open "python.org"
    exit 0
fi

# main
py -m pip install wget MuyunxiSupports BeautifulSoup4
py main.py
