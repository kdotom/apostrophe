window.addEventListener('load', function() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const formattedData = data.map(d => [d.Source, d.Destination, d['Monthly Payment']]);
            anychart.onDocumentReady(function() {
                // create a chart
                var chart = anychart.sankey();
                // set the data
                chart.data(formattedData);
                // set the container id
                chart.container('sankey-chart');
                // initiate drawing the chart
                chart.draw();
            });
        });
});
