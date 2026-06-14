# Compound Calculator [Dashboard](https://compound-calculator.streamlit.app/)

A **Streamlit** based dashboard that aggregates a collection of financial calculators for compound interest, EMI, loan pre‑payment, SIP, and more.  Users can select a calculator from the sidebar, adjust parameters using sliders or precise number inputs, and instantly see the results.

---

## Features

- **Multiple calculators** bundled under a single UI (see the `finance/` package).
- **Dual input controls** – a slider for quick selection and a number input for fine‑tuned values, kept in sync via Streamlit `session_state`.
- Automatic handling of type‑matching for Streamlit widgets (int/float consistency).
- Clean, responsive layout using Streamlit’s wide mode and column layout.

---

## Installation

```bash
# Clone the repository
git clone "https://github.com/DevBhuyan/Compound"
cd "Compound"

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`). Use the sidebar to pick a calculator, adjust the inputs, and view the results.

---

## Project Structure

```
.
├── app.py
├── calculators.py
├── decision
│   ├── goal_based_sip.py
│   ├── loan_vs_invest.py
│   ├── prepay_vs_invest.py
│   └── rent_vs_buy.py
├── finance
│   ├── emi.py
│   ├── loan_prepayment.py
│   ├── lumpsum.py
│   ├── repayment_schedule.py
│   └── sip.py
├── LICENSE
├── README.md
├── requirements.txt
```

---

## Adding a New Calculator

1. Create a new module in the `finance/` directory implementing a `calculate(**kwargs)` function.
2. Add an entry to `calculators.py` with the required input configuration (label, widget type, defaults, etc.).
3. The dashboard will automatically pick it up via the sidebar.

---

## License

This project is licensed under the **Apache 2.0 License** – see the `LICENSE` file for details.

---

## Contributing

Feel free to open issues or submit pull requests. Contributions that add new calculators, improve UI/UX, or enhance documentation are welcome.
