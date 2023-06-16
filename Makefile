# This is command "launcher". Used to launch training, model, tests, etc... #

#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y neet || :
	@pip install -e .

run_preprocess:
	python -c 'from neet.interface.main import preprocess; preprocess(source_type="train"); preprocess(source_type="val")'

run_train:
	python -c 'from neet.interface.main import train; train()'

run_pred:
	python -c 'from neet.interface.main import pred; pred()'

run_evaluate:
	python -c 'from neet.interface.main import evaluate; evaluate()'

run_all: run_preprocess run_train run_pred run_evaluate

run_model: run_all

#################### STREAMLIT ###################

# to be added here #

run_api:
	@streamlit run /home/aygul_unix/Projects/dssg2023_neet/neet/streamlit_api/app.py

#################### TESTS ###################

test:
	@pytest -v tests

#################### DATA SOURCES ACTIONS ###################
