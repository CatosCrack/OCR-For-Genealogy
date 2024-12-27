document.addEventListener('DOMContentLoaded', async function () {
    
    // Get data from sessionStorage
    const results = JSON.parse(sessionStorage.getItem('results'));

    // Get result container to add result components
    const container = document.getElementById('results_list');

    // Check if sessionStorage is empty
    if (results !== null){

        var i = 0;

        // Loop through each result and add it to the container
        results.forEach(result => {

            // Create result
            const resultRow = document.createElement('row');
            resultRow.className = "row d-flex justify-content-center align-items-center mt-4 mb-4";
            resultRow.id = "result_" + i++;
            resultRow.innerHTML = `
                <!-- Individual Result -->
                    <!-- Image -->
                    <div class="col-4 d-flex" id="result_image">
                        <img src="images/1.jpg">
                        <a href=${"viewer.html?id="+resultRow.id}><button id="view_button">Abrir documento</button></a>
                    </div>
                <!-- Data -->
                <div class="col-8 d-flex flex-column" id="data">
                    <div class="row mb-4">
                        <h3><a href=${"viewer.html?id="+resultRow.id} style="color: #173753;">${result["name"]}</a></h3>
                    </div>
                    <!-- Municipality Row -->
                    <div class="row">
                        <div class="col-4">
                            <h4>Municipio</h4>
                        </div>
                        <div class="col-8">
                            <p>${result["municipality"]}</p>
                        </div>
                    </div>
                    <!-- Department Row -->
                    <div class="row">
                        <div class="col-4">
                            <h4>Departamento</h4>
                        </div>
                        <div class="col-8">
                            <p>${result["department"]}</p>
                        </div>
                    </div>
                    <!-- Year Row -->
                    <div class="row">
                        <div class="col-4">
                            <h4>Año</h4>
                        </div>
                        <div class="col-8">
                            <p>${result["year"]}</p>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(resultRow);
        });
    } else {
        const resultRow = document.createElement('row');
        resultRow.className = "row d-flex justify-content-center align-items-center mt-4 mb-4";
        resultRow.id = "no_result";
        resultRow.innerHTML = `
            <h3>No se encontraron resultados</h3>
        `;
        container.appendChild(resultRow);
    }
});