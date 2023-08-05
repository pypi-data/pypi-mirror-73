from dotenv import load_dotenv, find_dotenv

def setup_testing_environment():
    load_dotenv(find_dotenv('.env', raise_error_if_not_found=True))
