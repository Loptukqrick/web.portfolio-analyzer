import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';

// third-party
import ReactApexChart from 'react-apexcharts';

// chart options
const areaChartOptions = {
    chart: {
        height: 450,
        type: 'area',
        toolbar: {
            show: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 2
    },
    grid: {
        strokeDashArray: 0
    }
};

// ==============================|| INCOME AREA CHART ||============================== //

const IncomeAreaChart = ({ slot }) => {
    const theme = useTheme();

    const { primary, secondary } = theme.palette.text;
    const line = theme.palette.divider;

    const [options, setOptions] = useState(areaChartOptions);

    useEffect(() => {
        setOptions((prevState) => ({
            ...prevState,
            colors: [theme.palette.primary.main, theme.palette.primary[700]],
            xaxis: {
                categories:
                    slot === 'month'
                        ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                labels: {
                    style: {
                        colors: [
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary,
                            secondary
                        ]
                    }
                },
                axisBorder: {
                    show: true,
                    color: line
                },
                tickAmount: slot === 'month' ? 11 : 7
            },
            yaxis: {
                labels: {
                    style: {
                        colors: [secondary]
                    }
                }
            },
            grid: {
                borderColor: line
            },
            tooltip: {
                theme: 'light'
            }
        }));
    }, [primary, secondary, line, theme, slot]);

    // TODO: acrodemocide -- figure out if we want more than one index to compare against
    const [series, setSeries] = useState([
        {
            name: 'Personal Portfolio',
            // TODO: acrodemocide - Figure out why we can't have more than 7 data points in this case
            data: [25, 50, 75, 100, 110, 130, 150] // , 155]
        },
        {
            name: 'S&P 500',
            data: [25, 35, 55, 40, 65, 88, 98] // , 106]
        }
        // {
        //     name: 'Dow Jones',
        //     data: [25, 20, 45, 35, 66, 69, 75] // , 64]
        // },
        // {
        //     name: 'NASDAQ',
        //     data: [25, 60, 50, 58, 72, 105, 88] // , 136]
        // }
    ]);

    // TODO: acrodemocide - Figure out how to have more than two colors for the charts.
    useEffect(() => {
        setSeries([
            {
                name: 'Personal Portfolio',
                data: slot === 'month' ? [25, 50, 75, 108, 120, 95, 135, 140, 155, 122, 145, 160] : [25, 50, 75, 100, 110, 130, 150] //, 155]
            },
            {
                name: 'S&P 500',
                data: slot === 'month' ? [25, 43, 55, 66, 60, 77, 68, 75, 88, 95, 100, 110] : [25, 35, 55, 40, 65, 88, 98] // , 106]
            }
            // {
            //     name: 'Dow Jones',
            //     data: slot === 'month' ? [25, 20, 48, 67, 58, 88, 95, 105, 110, 120, 89, 72] : [25, 20, 45, 35, 66, 69, 75] // , 64]
            // },
            // {
            //     name: 'NASDAQ',
            //     data: slot === 'month' ? [25, 120, 105, 100, 98, 94, 86, 81, 76, 73, 63, 41] : [25, 60, 50, 58, 72, 105, 88] // , 136]
            // }
        ]);
    }, [slot]);

    return <ReactApexChart options={options} series={series} type="area" height={450} />;
};

IncomeAreaChart.propTypes = {
    slot: PropTypes.string
};

export default IncomeAreaChart;
