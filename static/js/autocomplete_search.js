createAutocomplete = (selector, debounceTime) => {
    let count = 0

    new Autocomplete(selector, {
        search: input=> {
            const url = `/get_member_search_list/?search=${input}`
            return new Promise((resolve, reject)=> {
                fetch(url)
                .then(response => response.json())
                .then(response => {
                    resolve(response.payload);
                })
            })
        },
        debounceTime: debounceTime,
        renderResult: (result, props) => {
        return `
            <li ${props}>
                <div class="wiki-title d-flex flex-column justify-content-between">
                    <span>${result.member_name}</span>
                    <small class="text-muted">${result.member_phone}</small>
                </div>
            </li>
        `;
        },
        getResultValue: result => result.member_phone,
    })
}

createAutocomplete('#autocomplete_container', 500)