const SENTENCES = [];
const MATCHES = [];

class SpaceUnit {}; // unit for blocking matching on space characters

const colors = ["#00FFFF", "#0000FF", "#FF00FF", "#808080", "#008000", "#00FF00", "#800000", "#000080", "#808000", "#800080", "#FF0000", "#C0C0C0", "#008080", "#FFFF00", "#000000"];

function full_refresh_display () {
    const table = document.getElementById('strs');

    while (table.children.length>1) table.removeChild(table.lastChild);

    const matched_units = MATCHES.map(e=>e.unit);

    function get_color (unit) {
        if (matched_units.length==0) return '#000000';
        if (unit===null) return '#000000';
        return colors.at(matched_units.indexOf(unit)%colors.length);
    }

    function color (uk_str, mask=null) {
        if (mask==null) mask = new Array(uk_str.length).fill(null);
        out = '';
        for (const i in uk_str)
            out += `<font color=${get_color(mask[i])}>${uk_str[i]}</font>`;
        return out;
    }

    for (const sentence of SENTENCES) {
        const tr = document.createElement('tr');

        tr.appendChild(Object.assign(document.createElement('td'), {innerHTML:color(sentence.uk_str,sentence.uk_mask)}));
        tr.appendChild(Object.assign(document.createElement('td'), {textContent:sentence.k_str}));
        td_units = document.createElement('td');
        for (const unit of sentence.k_units||[]) {
            td_units.appendChild(Object.assign(document.createElement('font'), {textContent:unit,classList:['unit'],color:get_color(unit)}));
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

    document.getElementById('uk_str_remove_puncts').addEventListener('click', () => {
        for (const sentence of SENTENCES) {
            sentence.uk_str = clean_str(sentence.uk_str, document.getElementById('chars_delete').value);
            sentence.uk_mask = new Array(sentence.uk_str.length).fill(0).map((e,i)=>(sentence.uk_str[i]==" "?new SpaceUnit():null));
        }

        full_refresh_display();
    });
    document.getElementById('k_str_remove_majs').addEventListener('click', () => {
        for (const sentence of SENTENCES)
            sentence.k_str = clean_str(sentence.k_str, document.getElementById('chars_delete').value);
        full_refresh_display();
    });
    document.getElementById('uk_str_remove_majs').addEventListener('click', () => {
        for (const sentence of SENTENCES)
            sentence.uk_str = sentence.uk_str.toLowerCase();
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

document.getElementById('units_extract').addEventListener('click', () => {
    switch (document.getElementById('units_method').value) {
        case 'units_words':
            for (const sentence of SENTENCES)
                sentence.k_units = new Set(sentence.k_str.split(/[\s\t]+/));
            full_refresh_display();
            break;
        case 'morphemes': // TODO
            for (const sentence of SENTENCES) {
                const k_units = new Set();
                for (const word of sentence.k_str.split(/[\s\t]+/))
                    (ENGLISH_MORPHEMES[word].slice(0,1)||[word]).forEach(unit => {
                        k_units.add(unit);
                    });
                sentence.k_units = k_units;
            }
            full_refresh_display();
            break;
    }
});

function reset_matching () {
    while (MATCHES.length) MATCHES.pop();

    for (const sentence of SENTENCES) {
        sentence.uk_mask = new Array(sentence.uk_str.length).fill(0).map((e,i)=>(sentence.uk_str[i]==" "?new SpaceUnit():null));
        sentence.unmatched_k_units = new Set(sentence.k_units);
    }

    full_refresh_display();
}

document.getElementById('reset_matching').addEventListener('click', () => {
    reset_matching();
})

document.getElementById('automatic_matching').addEventListener('click', () => {

    let new_match = true;
    while (new_match!==undefined) {
        new_match = FindBestMatch(SENTENCES, MATCHES)[0];
        if(new_match!==undefined) {
            apply_match(SENTENCES, new_match);
            MATCHES.push(new_match);
        }
    }

    console.table(MATCHES);

    full_refresh_display();
});

document.getElementById('matching_step').addEventListener('click', () => {

    const selector = document.getElementById('possible_matches');
    while (selector.childElementCount) selector.removeChild(selector.firstChild);

    const possible_matches = FindBestMatch(SENTENCES, MATCHES);
    for (const match of possible_matches) {
        selector.appendChild(Object.assign(document.createElement('option'), {
            value: JSON.stringify(match),
            innerHTML: `<b>${match.uk_unit}</b> <-> ${match.unit} (Score: ${match.score})`
        }));
    }
})

document.getElementById('apply_match').addEventListener('click', () => {
    const selector = document.getElementById('possible_matches');
    if (selector.value=='') return;
    const new_match = JSON.parse(selector.value);
    apply_match(SENTENCES, new_match);
    MATCHES.push(new_match);
    while (selector.childElementCount) selector.removeChild(selector.firstChild);
    full_refresh_display();
});