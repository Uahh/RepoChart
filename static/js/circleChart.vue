<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="circle" class="chart"></div>
                <el-row>
                    <el-col :span="12">
                    </el-col>
                    <el-col :span="12">
                        <div class="radio">
                            <a style="padding: 10px">Order by:</a>
                            <el-radio v-model="radio" label="$commits" border size="medium" @change="rerun()">
                                commits
                            </el-radio>
                            <el-radio v-model="radio" label="$lines" border size="medium" @change="rerun()">
                                lines
                            </el-radio>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </el-col>
    </el-row>
</template>
 
<script>
module.exports = {
    data() {
        return {
            radio: "$commits",
            dataStatus: false,
            data: null,
            // myChart: null,
            option: null
        };
    },
    props: {
        repo: null,
        server: null
    },
    mounted: function () {
        this.circleEchartsInit();
    },
    methods: {
        circleEchartsInit() {
            console.log(this.server)
            console.log(this.repo)
            this.init()
            this.myChart.showLoading();
            if (this.dataStatus == false) {
                this.times = setInterval(this.getData(), 3000);
            }
            this.option && this.myChart.setOption(this.option);
        },
        init() {
            this.myChart = echarts.init(document.getElementById('circle'))
        },
        getData() {
            let status;
            $.ajax({
                type: "post",
                url: 'http://' + this.server + '/repochart/check',
                data: {
                    repo: this.repo
                },
                async: false,
                success: function (result) {
                    status = result.status;
                }
            })
            if (status == 'True') {
                this.dataStatus = true
                clearInterval(this.times);
                $.ajax({
                    type: "post",
                    url: 'http://' + this.server + '/repochart/chartdata',
                    data: {
                        type: 'circle',
                        repo: this.repo
                    },
                    async: false,
                    dataType: 'json',
                    success: (result) => {
                        this.data = result;
                        $.when(
                            $.getScript(
                                'https://d3js.org/d3-hierarchy.v2.min.js'
                            )
                        ).done(() => {
                            this.run();
                            this.myChart.hideLoading();
                        });
                    }
                })
            }
            return this.getData;
        },
        run() {
            const dataWrap = this.prepareData();
            this.initChart();
        },
        prepareData() {
            const seriesData = [];
            let maxDepth = 0;
            var radio = this.radio;
            function convert(source, basePath, depth) {
                if (source == null) {
                    return;
                }
                if (maxDepth > 10) {
                    return;
                }
                maxDepth = Math.max(depth, maxDepth);
                seriesData.push({
                    id: basePath,
                    value: source[radio],
                    color: source['$color'],
                    url: source['$url'],
                    depth: depth,
                    index: seriesData.length
                });
                for (var key in source) {
                    if (source.hasOwnProperty(key) && !key.match(/^\$/)) {
                        var path = basePath + '/' + key;
                        convert(source[key], path, depth + 1);
                    }
                }
            }
            convert(this.data, this.repo.split('/')[1], 0);
            this.seriesData = seriesData
        },
        stratify() {
            return d3
                .stratify()
                .parentId(function (d) {
                    return d.id.substring(0, d.id.lastIndexOf('/'));
                })(this.seriesData)
                .sum(function (d) {
                    return d.value || 0;
                })
                .sort(function (a, b) {
                    return b.value - a.value;
                });
        },
        initChart() {
            this.displayRoot = this.stratify();
            this.option = {
                title: {
                    text: this.repo_name,
                },
                dataset: {
                    source: this.seriesData
                },
                tooltip: {},
                toolbox: {
                    show: true,
                    bottom: '1%',
                    left: '1%',
                    itemSize: 20,
                    feature: {
                        saveAsImage: {
                            show: true
                        }
                    }
                },
                hoverLayerThreshold: Infinity,
                series: {
                    type: 'custom',
                    renderItem: this.renderItem,
                    progressive: 0,
                    coordinateSystem: 'none',
                    encode: {
                        tooltip: 'value',
                        itemName: 'id'
                    },
                    itemStyle: {
                        color: function (param) {
                            return param.data.color;
                        },
                        borderWidth: 5
                    },
                }
            };
            this.myChart.setOption(this.option);
            this.myChart.on('click', { seriesIndex: 0 }, (params) => {
                this.drillDown(params.data.id);
            });

            this.myChart.on('dblclick', { seriesIndex: 0 }, (params) => {
                if (!params.event.topTarget.textConfig) {
                    window.open(this.seriesData[params.value.index].url)
                }
            });
            // Reset: click on the blank area.
            this.myChart.getZr().on('click', (event) => {
                if (!event.target) {
                    this.drillDown();
                }
            });
        },
        renderItem(params, api) {
            var context = params.context;
            // Only do that layout once in each time `setOption` called.
            if (!context.layout) {
                context.layout = true;
                // overallLayout(params, api);
                var context = params.context;
                d3
                    .pack()
                    .size([api.getWidth() - 2, api.getHeight() - 2])
                    .padding(3)(this.displayRoot);
                context.nodes = {};
                this.displayRoot.descendants().forEach(function (node, index) {
                    context.nodes[node.id] = node;
                });
            }
            var nodePath = api.value('id');
            var node = context.nodes[nodePath];
            if (!node) {
                // Reder nothing.
                return;
            }
            var isLeaf = !node.children || !node.children.length;
            var focus = new Uint32Array(
                node.descendants().map(function (node) {
                    return node.data.index;
                })
            );
            var nodeName = isLeaf
                ? nodePath
                    .slice(nodePath.lastIndexOf('/') + 1)
                    .split(/(?=[A-Z][^A-Z])/g)
                    .join('\n')
                : '';
            var z2 = api.value('depth') * 2;
            return {
                type: 'circle',
                focus: focus,
                shape: {
                    cx: node.x,
                    cy: node.y,
                    r: node.r
                },
                transition: ['shape'],
                z2: z2,
                textContent: {
                    type: 'text',
                    style: {
                        // transition: isLeaf ? 'fontSize' : null,
                        text: nodeName,
                        fontFamily: 'Arial',
                        width: node.r * 1.3,
                        overflow: 'truncate',
                        fontSize: node.r / 4
                    },
                    emphasis: {
                        style: {
                            overflow: null,
                            fontSize: Math.max(node.r / 4, 12)
                        }
                    }
                },
                textConfig: {
                    position: 'inside'
                },
                style: {
                    fill: api.visual('color'),
                    stroke: '#444444',
                    lineWidth: 1,
                },
                emphasis: {
                    style: {
                        fontFamily: 'Arial',
                        fontSize: 12,
                        stroke: '#000000',
                        lineWidth: 1,
                        shadowBlur: 20,
                        shadowOffsetX: 3,
                        shadowOffsetY: 5,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            };
        },
        drillDown(targetNodeId) {
            if (targetNodeId == undefined && this.displayRoot != undefined) {
                // let id = this.displayRoot.data.id.substring(0, this.displayRoot.data.id.length - 1)
                let pos = this.displayRoot.data.id.lastIndexOf('/')
                targetNodeId = this.displayRoot.data.id.substr(0, pos + 1)
                targetNodeId = targetNodeId.substring(0, targetNodeId.length - 1)
            }
            if (targetNodeId != null) {
                this.displayRoot = this.stratify();
                this.displayRoot = this.displayRoot.descendants().find(function (node) {
                    return node.data.id === targetNodeId;
                });
            }
            // A trick to prevent d3-hierarchy from visiting parents in this algorithm.
            if (this.displayRoot != undefined) {
                this.displayRoot.parent = null;
                this.myChart.setOption({
                    dataset: {
                        source: this.seriesData
                    }
                });
            }
        },
        rerun() {
            this.run()
        }
    }
}
</script>
 
<style>
.radio {
    text-align: right;
    /* width: 250px; */
}
</style>