const options = {
    data() {
        return {
            activeName: 'circle'
        };
    },
    methods: {
        handleClick(){
        },
        handleSelect(key, keyPath) {
            console.log(1);
            console.log(keyPath);
        },
    },
    moduleCache: {
        vue: Vue
    },
    async getFile(url) {
        const res = await fetch(url);
        if (!res.ok)
            throw Object.assign(new Error(res.statusText + ' ' + url), { res });
        return {
            getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
        }
    },
    addStyle(textContent) {

        const style = Object.assign(document.createElement('style'), { textContent });
        const ref = document.head.getElementsByTagName('style')[0] || null;
        document.head.insertBefore(style, ref);
    },
    components: {
        'circle-chart': Vue.defineAsyncComponent(() => loadModule('../static/js/circleChart.vue', options)),
        'square-chart': Vue.defineAsyncComponent(() => loadModule('../static/js/squareChart.vue', options)),
        'line-chart': Vue.defineAsyncComponent(() => loadModule('../static/js/starLineChart.vue', options)),
        'commit-size-line-chart': Vue.defineAsyncComponent(() => loadModule('../static/js/commitSizeLineChart.vue', options)),
        'commit-size-pie-chart': Vue.defineAsyncComponent(() => loadModule('../static/js/commitSizePieChart.vue', options)),
        
    },
}

const { loadModule } = window['vue3-sfc-loader'];

const V = Vue.createApp(options);

V.use(ElementPlus);
V.mount("#app");