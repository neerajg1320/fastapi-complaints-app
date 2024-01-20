# To run the app
uvicorn main:app

export PYTHONPATH=./
python commands/create_super_user.py -f Test -l Admin -e geo@abc.com -p 123456789 -i GBW2333243 -pa Local123