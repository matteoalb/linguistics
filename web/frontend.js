const SENTENCES = [];

function full_refresh_display () {
    const table = document.getElementById('strs');

    while (table.children.length>1) table.removeChild(table.lastChild);

    for (const sentence of SENTENCES) {
        const tr = document.createElement('tr');
        tr.appendChild(Object.assign(document.createElement('td'), {textContent:sentence.uk_str}));
        tr.appendChild(Object.assign(document.createElement('td'), {textContent:sentence.k_str}));
        td_units = document.createElement('td');
        for (const unit of sentence.k_units||[]) {
            td_units.appendChild(Object.assign(document.createElement('font'), {textContent:unit,classList:['unit']}))
        }
        tr.appendChild(td_units)
        table.appendChild(tr);
    }
}

{ // IMPORT CSV
    const csv_import = document.getElementById('csv_import');
    csv_import.addEventListener('input', async (e)=>{

        if (csv_import.files.length) {
            const separator = document.getElementById('csv_separator').value;

            const pairs = [];
            for (const line of (await csv_import.files[0].text()).split(/[\r\n]+/)) {
                const [uk_str,k_str] = line.split(separator);
                if (k_str) pairs.push({uk_str,k_str});
            }

            for ({uk_str,k_str} of pairs) {
                SENTENCES.push({
                    uk_str, k_str
                });
            }

            full_refresh_display();
        }
    });
}

{ // CLEAN INPUT

    function clean_str (str, chars) {
        for (const char of chars)
            str = str.replaceAll(char, ' ');
        return str
            // .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g," ")
            .replace(/[\s\t]+/," ").trim();
    }

    document.getElementById('uk_str_remove_majs').addEventListener('click', () => {
        for (const sentence of SENTENCES)
            sentence.uk_str = clean_str(sentence.uk_str, document.getElementById('chars_delete').value);
        full_refresh_display();
    });
    document.getElementById('k_str_remove_majs').addEventListener('click', () => {
        for (const sentence of SENTENCES)
            sentence.k_str = clean_str(sentence.k_str, document.getElementById('chars_delete').value);
        full_refresh_display();
    });


    document.getElementById('k_english_str_remove_majs').addEventListener('click', () => {
        for (const sentence of SENTENCES)
            sentence.k_str = clean_str(
                sentence.k_str.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g," "),
                ".,;:!?_-[](){}").toLowerCase();
        full_refresh_display();
    });
}

// STEPS
function step_csv () {
    [...document.querySelectorAll('.menu')].forEach(e=>e.classList.add('hidden'));
    document.getElementById('step_csv').classList.remove('hidden');
}
function step_units () {
    [...document.querySelectorAll('.menu')].forEach(e=>e.classList.add('hidden'));
    document.getElementById('step_units').classList.remove('hidden');
}
function step_matching () {
    [...document.querySelectorAll('.menu')].forEach(e=>e.classList.add('hidden'));
    document.getElementById('step_matching').classList.remove('hidden');
}

class SpaceUnit {}; // unit for blocking matching on space characters

document.getElementById('units_extract').addEventListener('click', () => {
    switch (document.getElementById('units_method').value) {
        case 'units_words':
            for (const sentence of SENTENCES)
                sentence.k_units = new Set(sentence.k_str.split(/[\s\t]+/));
            full_refresh_display();
            break;
        case 'morphemes': // TODO
            for (const sentence of SENTENCES)
                sentence.k_units = new Set(sentence.k_str.split(/[\s\t]+/));
            full_refresh_display();
            break;
    }
});

