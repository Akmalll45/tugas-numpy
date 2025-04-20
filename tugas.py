from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def load_data():
    return np.genfromtxt('numpyyy.txt', delimiter='\t', names=True, dtype=None, encoding='utf-8')

@app.route('/', methods=['GET'])
def index():
    full_data = load_data()
    gender_filter = request.args.get('gender')

    # Jika filter gender digunakan
    if gender_filter:
        full_data = full_data[full_data['gender'] == gender_filter]

    display_data = full_data [:10]

    # Ambil list gender unik
    genders = sorted(set(row['gender'] for row in load_data()))

    # Hitung statistik jika kolom tersedia
    total_data = len(full_data)
    avg_math = np.mean(full_data['math_score']) if 'math_score' in full_data.dtype.names else 0
    avg_reading = np.mean(full_data['reading_score']) if 'reading_score' in full_data.dtype.names else 0
    avg_writing = np.mean(full_data['writing_score']) if 'writing_score' in full_data.dtype.names else 0

    # Distribusi gender
    gender_dist = {g: np.sum(load_data()['gender'] == g) for g in genders}

    return render_template('index.html',
                           data=display_data,
                           columns=full_data.dtype.names,
                           genders=genders,
                           total_data=total_data,
                           avg_math=avg_math,
                           avg_reading=avg_reading,
                           avg_writing=avg_writing,
                           gender_dist=gender_dist)

if __name__ == '__main__':
    app.run(debug=True)
