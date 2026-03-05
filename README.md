# Fantasy Football Draft Simulator

A web-based fantasy football draft simulator that lets you:

- Sort and filter players by position, fantasy points, and league scoring (PPR, Half PPR, Standard)
- Adjust default and save your custom rankings by position
- Draft against an AI trained on positional rankings for each league type
- Support multiple positions including QB, RB, WR, TE, FLEX, Super FLEX, D/ST, and K
- Customize fantasy league settings including TE premium, 8, 10 or 12 players, and custom position requirements
- Save draft results for later review

## Backend Setup (Python + FastAPI)

### 1. Navigate to the backend folder

```bash
cd backend
```

### 2. Create virtual environment and activate it

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### 3. Upgrade pip, setuptools, and wheel

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the backend server

```bash
python -m uvicorn app.main:app --reload
```

## Frontend Setup (React + TypeScript)

### 1. Navigate to frontend folder

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the frontend server

```bash
npm start
```
