
    document.addEventListener("DOMContentLoaded", function () {

        const tableBody = document.querySelector("#device_table tbody");
        const addBtn = document.getElementById("add_row");

        // Add new row
        addBtn.addEventListener("click", function () {
            let newRow = document.createElement("tr");

            newRow.innerHTML = `
                <td><input name="model_number[]" class="form-control"/></td>
                <td><input name="serial_number[]" class="form-control"/></td>
                <td><input name="description[]" class="form-control"/></td>
                <td><button type="button" class="btn btn-danger remove_row">X</button></td>
            `;

            tableBody.appendChild(newRow);
        });

        // Remove row (event delegation)
        tableBody.addEventListener("click", function (e) {
            if (e.target.classList.contains("remove_row")) {
                let row = e.target.closest("tr");
                if (tableBody.children.length > 1) {
                    row.remove();
                }
            }
        });

    });
