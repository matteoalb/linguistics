
const base = 257n;
const mod = (1n<<61n)-1n;

function powMod(base, exponent, modulus){
    
    /*
        Modular Exponentiation by adrian154 on GitHub
    */

    if(modulus == 1n) {
        return 0n;
    }

    let result = 1n;
    base = base % modulus;
    while(exponent > 0n) {
        if(exponent % 2n == 1n) {
            result = (result * base) % modulus;
        }
        exponent >>= 1n;
        base = (base * base) % modulus;
    }
    
    return result;

}

function hashes(s, mask, length){
    let result = new Map();
    let h = 0n; let valid = 0;

    let power = powMod(base, BigInt(length), mod);

    for (let i = 0; i < s.length; i++) {
        h = (h * base + BigInt(s.charCodeAt(i))) % mod;
        valid += (mask[i]==null);

        if(i >= length){
            h = ((h - BigInt(s.charCodeAt(i-length)) * power) % mod + mod) % mod;
            valid -= (mask[i-length]==null);
        }

        if(i>=length-1 && valid === length){
            if (!result.has(h)) result.set(h, []);
            result.get(h).push(i - length + 1);
        }
    }

    return result;
}

function LCS(strings, masks=null) {
    /*
        Returns the longest common subrstring in a list of strings
    */
    strings = Array.from(strings);

    if(strings.length === 0){
        return ""
    }

    if(masks === null){
        masks = strings.map(s => new Array(s.length).fill(null));
    }
    else{
        masks = masks.map(m => Array.from(m));
    }

    if(masks.length !== strings.length || strings.some((s, i) => s.length !== masks[i].length)){
        throw new Error("Each string must have a matching mask.");
    }

    function check(length){
        let first = hashes(strings[0], masks[0], length);
        const others = strings.slice(1).map((s, i) => hashes(s, masks[i + 1], length));

        for(let [h, positions] of first){
            for(let i=0; i<positions.length; i++){
                const pos = positions[i];
                const candidate = strings[0].slice(pos,pos+length);
                const result = strings.slice(1).every((s, i) => {
                    const hs = others[i]; 
                    const indices = (hs instanceof Map ? hs.get(h) : hs[h]) ?? [];
                    return indices.some(p => s.slice(p, p + length) === candidate);
                });
                if(result){
                    return candidate;
                }
            }
        }
        return null;
    }

    let low = 1;
    let high = Math.min(...strings.map(s => s.length));

    let answer = "";

    while(low <= high){
        let mid = Math.floor((low + high) / 2);
        let result = check(mid);

        if(result !== null){
            answer = result;
            low = mid +1;
        }
        else{
            high = mid - 1;
        }
    }
    return answer;
}

function* KMP_occ(substr, str){
    /*
        Knuth-Morris-Pratt algorithm
    */
    function LPS(str){
        /*
            Computes the Longest Prefix Suffix of the KPM algorithm
        */
        let k=0;
        let arr = new Array(str.length).fill(0);
        let i = 1;
        while (i<str.length){
            if(str[i]===str[k]){
                k+=1;
                arr[i]=k;
                i+=1;
            }
            else{
                if(k>0){
                    k = arr[k-1];
                }
                else{
                    arr[i] = 0;
                    i+=1;
                }
            }
        }
        return arr;
    }
    let arr = LPS(substr + "\0" + str);
    for(let i=2*substr.length;i<arr.length; i++){
        if(arr[i]===substr.length){
            yield i  - 2* substr.length;
        }
    }
}

function PreProcessSentences(raw){
    /*
        Slice the sentences in the know language into units
    */
    const processed = new Array(raw.length);

    for(let i=0; i < raw.length; i++){
        let uk_str = raw[i][0];
        let k_str = raw[i][1];

        const k_str_units = new Set(k_str.replaceAll(".", "").split(" ").map(x => x.toLowerCase()));

        processed[i] = [uk_str, k_str_units, [...uk_str].map(s => s !== " ")];
    }

    return processed;
}

const unzip = (arr) => {
    if (arr.length === 0) return [];
    return arr[0].map((_, colIndex) => arr.map(row => row[colIndex]));
};

function score_function(uk_guess_len, nb_intersect_sentences){
    return .5 * Math.log(uk_guess_len) + .3 * Math.log(nb_intersect_sentences);
}

function FindBestMatch(sentences, known_matches){
    /*
        Returns the best match between a unit in English and
        a morpheme in the unknown language
    */
    const all_units = new Set();
    for(let i =0; i < sentences.length; i++){
        for(let item of sentences[i].unmatched_k_units){
            all_units.add(item);
        }
    }

    const possible_matches = new Array();

    for(let unit of all_units){
        let unique_uk_candidates = new Array();
        let possible_units = new Set(all_units);

        for(const sentence of sentences){
            if(sentence.unmatched_k_units.has(unit)){
                possible_units = new Set([...sentence.unmatched_k_units].filter(x => possible_units.has(x)));
                unique_uk_candidates.push([sentence.uk_str, sentence.uk_mask]);
            }
        }

        if(possible_units.size === 1){
            const [strs, masks] = unzip(unique_uk_candidates);
            let uk_guess = LCS(strs, masks).trim();
            if(uk_guess !== ""){
                let score = score_function(uk_guess.length, unique_uk_candidates.length)
                possible_matches.push({score, uk_unit:uk_guess, unit});
            }
        }
    }

    possible_matches.sort((a,b) => b.score-a.score);

    return possible_matches;
}

function apply_match (sentences, match) {

    const {uk_unit,unit} = match;

    // known_matches.push([uk_unit, unit]);


    for(let i = 0; i<sentences.length; i++){
        let {uk_str, unmatched_k_units, uk_mask} = sentences[i];
        if(unmatched_k_units.has(unit)){
            // console.log(JSON.stringify(sentences[i].uk_mask));
            unmatched_k_units.delete(unit);
            for(let s of KMP_occ(uk_unit,uk_str)){
                let unused = true;
                for(let j=s; j<s+uk_unit.length;j++)
                    unused &&= (uk_mask[j]==null);
                if (unused)
                    for(let j=s; j<s+uk_unit.length;j++)
                        uk_mask[j]=unit;
            }
            // console.log(JSON.stringify(sentences[i].uk_mask));
        }
        // sentences[i] = [uk_str, k_units, uk_mask];
    }

    // return [uk_unit, unit] // New match
}



/*
const SENTENCES_RAW = [
    ["Ko nakonako ŋkoe","you are walking"],
    ["E nakonako te aiine","a woman is walking"],
    ["I takaakaro ŋai","I am playing"],
    ["E nakonako nakon te titooa Meeri","Mary is walking to the store"],
    ["A tekateka irarikin te auti aiine","women are sitting next to the house"],
    ["A tebotebo nakekei n te bong aei","people are bathing today"],
    ["I tebotebo inanon te auti ŋai","I am bathing in the house"],
    ["A takaakaro inanon te titooa ataei","children are playing in the store"],
    ["Ko tekateka ŋkoe ningaabong","you will sit tomorrow"]
]

const SENTENCES = PreProcessSentences(SENTENCES_RAW);

console.log();
const matches = new Array();
let new_match = true;
while(new_match!==undefined){
    //console.log();
    new_match = FindBestMatch(SENTENCES, matches)[0];

    if(new_match!==undefined)
        apply_match(SENTENCES, new_match)
}
console.log(matches);
*/