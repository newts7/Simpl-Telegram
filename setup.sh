pip install -r requirements.txt
git clone https://github.com/bitly/bitly-api-python.git
cd bitly-api-python
python setup.py install
cd ..
rm -rf bitly-api-python
echo "Setup done successfully"
