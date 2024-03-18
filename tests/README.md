How to execute unit test cases for this program ?

1. Create a virtual environment or activate it if already exists
2. At root of code directory run below command
3. pip install coverage
3. coverage run -m unittest discover -s tests -p "*test_*.py"
4. Genrate coverage report. run below command
5. coverage report
6. generate an HTML report for a more detailed view of the coverage. run below command
7. coverage html
8. Above command will generate a folder named htmlcov with coverage report
9. Inside htmlcov click on htmlcov/index.html

