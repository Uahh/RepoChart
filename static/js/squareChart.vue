<template>
    <div id="square" class="squareChart"></div>
</template>
 
<script>
module.exports = {
    data() {
        return {
        };
    },
    mounted: function () {
        this.squareEchartsInit();
    },
    methods: {
        squareEchartsInit() {
            var ROOT_PATH = '../../output/itorr/imouto_square.json';
            var chartDom = document.getElementById('square');
            var myChart = echarts.init(chartDom);
            var option;

            myChart.showLoading();
            $.get(ROOT_PATH, function (diskData) {
                myChart.hideLoading();
                function getLevelOption() {
                    return [
                        {
                            itemStyle: {
                                borderColor: '#333',
                                borderWidth: 0,
                                gapWidth: 1,
                            },
                            upperLabel: {
                                show: false
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#444',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#555',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#666',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#777',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#888',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#999',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#AAA',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#BBB',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            itemStyle: {
                                borderColor: '#CCC',
                                borderWidth: 5,
                                gapWidth: 1
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: '#ddd'
                                }
                            }
                        },
                        {
                            colorSaturation: [0.35, 1],
                            itemStyle: {
                                borderWidth: 5,
                                gapWidth: 1,
                                borderColorSaturation: 0.6
                            }
                        }
                    ];
                }
                myChart.setOption(
                    (option = {
                        title: {
                            text: 'Disk Usage',
                            left: 'center'
                        },
                        tooltip: {
                            formatter: function (info) {
                                var value = info.value;
                                var treePathInfo = info.treePathInfo;
                                var treePath = [];
                                for (var i = 1; i < treePathInfo.length; i++) {
                                    treePath.push(treePathInfo[i].name);
                                }
                                return [
                                    '<div class="tooltip-title">' +
                                    echarts.format.encodeHTML(treePath.join('/')) +
                                    '</div>',
                                    'Disk Usage: ' + echarts.format.addCommas(value) + ' KB'
                                ].join('');
                            }
                        },
                        series: [
                            {
                                name: 'Disk Usage',
                                type: 'treemap',
                                visibleMin: 300,
                                label: {
                                    show: true,
                                    formatter: '{b}'
                                },
                                upperLabel: {
                                    show: true,
                                    height: 30
                                },
                                itemStyle: {
                                    borderWidth: 5
                                },
                                levels: getLevelOption(),
                                data: diskData
                            }
                        ]
                    })
                );
            });

            option && myChart.setOption(option);
        },
    }
}
</script>
 
<style>
.squareChart {
    height: 800px;
    width: 100%;
}
</style>