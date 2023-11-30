# Storage task

## Installing using GitHub:

1. Clone the repository:

```bash
git clone https://github.com/KittNeKit/storage_task
```
2. Change to the project's directory:
```bash
cd storage_task
```
3. Once you're in the desired directory, run the following command to create a virtual environment:
```bash
python -m venv venv
```
4. Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

5. Install the dependencies

```bash
pip install -r requirements.txt
```

6. Start the development server

```bash
 uvicorn app.main:app --reload
```

7. Access the website locally at http://localhost:8000.
