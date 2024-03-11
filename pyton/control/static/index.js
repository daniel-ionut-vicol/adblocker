const mlserver_url = "http://192.168.69.207:8081"
listProcesses()
getLogs()
getEvaluationLogs()
getModels()

document.getElementById("get_logs").addEventListener("click", getLogs);
document.getElementById("get_evaluation_logs").addEventListener("click", getEvaluationLogs);
document.getElementById("list_processes").addEventListener("click", listProcesses)
document.getElementById("get_models").addEventListener("click", getModels);
document.getElementById("start_training").addEventListener("click", () => {
    // Send a POST request to the server to start the training
    fetch(mlserver_url + '/start_training', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message)
            console.log(data.message);
        })
        .catch((error) => {
            alert('Error:', error)
            console.error('Error:', error);
        }).finally(() => {
            listProcesses()
            getLogs()
        })
})

// Fetch the file contents from the server
fetch(mlserver_url + '/hyperparameters')
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(config => {
        // Create a form with an input field for each parameter in the configuration
        let form = '<form id="configForm">';
        for (const parameter in config) {
            if (parameter === 'MODEL') {
                // Create a select dropdown for the model
                form += `
            <label for="${parameter}">${parameter}:</label>
            <select id="${parameter}" name="${parameter}">
                <option value="RESNET50" ${config.MODEL === 'RESNET50' ? 'selected' : ''}>RESNET50</option>
                <option value="VGG16" ${config.MODEL === 'VGG16' ? 'selected' : ''}>VGG16</option>
                <option value="VGG19" ${config.MODEL === 'VGG19' ? 'selected' : ''}>VGG19</option>
                <option value="INCEPTION_V3" ${config.MODEL === 'INCEPTION_V3' ? 'selected' : ''}>INCEPTION_V3</option>
                <option value="XCEPTION" ${config.MODEL === 'XCEPTION' ? 'selected' : ''}>XCEPTION</option>
                <option value="EFFICIENTNET_B0" ${config.MODEL === 'EFFICIENTNET_B0' ? 'selected' : ''}>EFFICIENTNET_B0</option>
                <option value="MOBILENET" ${config.MODEL === 'MOBILENET' ? 'selected' : ''}>MOBILENET</option>
                <option value="DENSENET121" ${config.MODEL === 'DENSENET121' ? 'selected' : ''}>DENSENET121</option>
            </select>
            <br>
            `;
            } else {
                form += `
            <label for="${parameter}">${parameter}:</label>
            <input type="text" id="${parameter}" name="${parameter}" value="${config[parameter]}">
            <br>
            `;
            }
        }
        form += '<input type="submit" value="Update"></form>';


        // Add the form to the page
        document.getElementById('params').innerHTML = form;

        // Add an event listener to the form
        document.getElementById('configForm').addEventListener('submit', function (event) {
            event.preventDefault();

            // Get the new values from the input fields
            const newConfig = {};
            for (const parameter in config) {
                newConfig[parameter] = document.getElementById(parameter).value;
            }

            // Send a POST request to the server to update the configuration
            fetch(mlserver_url + '/update_config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newConfig),
            })
                .then(response => {
                    if (!response.ok) {
                        alert("Error: ", response)
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    alert("Success")
                    return response.json();
                })
                .then(data => {

                    console.log('Updated configuration:', data);
                    // Update the input fields with the updated values
                    for (const parameter in data) {
                        document.getElementById(parameter).value = data[parameter];
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        });
    })
    .catch(e => {
        console.log('There was a problem with the fetch operation: ' + e.message);
    });

function getEvaluationLogs() {
    // Send a GET request to the server to get the logs
    fetch(mlserver_url + '/get_evaluation_logs', {
        method: 'GET',
    })
        .then(response => response.text())
        .then(data => {
            // Create a preformatted text element to display the logs
            const pre = document.createElement('pre');
            pre.textContent = data;

            // Add the text element to the page
            document.getElementById('evaluation_logs').innerHTML = "<pre>" + data + "</pre>";
        })
        .catch((error) => {
            alert('Error:', error)
            console.error('Error:', error);
        });
}

function getLogs() {
    // Send a GET request to the server to get the logs
    fetch(mlserver_url + '/get_logs', {
        method: 'GET',
    })
        .then(response => response.text())
        .then(data => {
            // Create a preformatted text element to display the logs
            const pre = document.createElement('pre');
            pre.textContent = data;

            // Add the text element to the page
            document.getElementById('logs').innerHTML = "<pre>" + data + "</pre>";
        })
        .catch((error) => {
            alert('Error:', error)
            console.error('Error:', error);
        });
}

function createTree(container, obj) {
    if (typeof obj === 'object') {
        container.innerHTML = JSON.stringify(obj, null, 2)
            .replace(/: null/g, ': {}')
            .replace(/"/g, '')
            .replace(/,/g, '')
            .replace(/{/g, '<ul><li>')
            .replace(/}/g, '</li></ul>')
            .replace(/:/g, '</li><li>');
        container.firstChild.innerHTML = container.firstChild.innerHTML.replace(/<li>/g, '<li onclick="handleClick(this)">');
    } else {
        console.error('Unexpected data format:', obj);
    }
}

function handleClick(li) {
    const filePath = li.textContent.trim();
    fetch('/run_command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file_path: filePath }),
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => console.error('Error:', error));
}

function getModels() {
    fetch('/get_models')
        .then(response => response.json())
        .then(models => {
            const modelsContainer = document.getElementById('models');
            modelsContainer.innerHTML = '';  // Clear the existing contents
            createSubItems(models, modelsContainer);
        });
}

function createSubItems(node, parentElement, path = '') {
    for (const item in node) {
        const newPath = path ? `${path}/${item}` : item;
        if (node[item] === null) {
            // If the item is a file
            if (item.endsWith('.h5')) {
                // Create a new div element
                const div = document.createElement('div');
                div.className = 'flex-container';

                // Create a new model element (p tag)
                const modelElement = document.createElement('p');
                modelElement.textContent = item;
                modelElement.className = 'model';

                // Create a new button element
                const button = document.createElement('button');
                button.textContent = 'Test';
                button.className = 'test-button';
                button.onclick = function () {
                    fetch('/start_testing', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ model: newPath }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            alert('Success:', data);
                            console.log('Success:', data);
                        })
                        .catch((error) => {
                            alert('Error:', error);
                            console.error('Error:', error);
                        }).finally(() => {
                            listProcesses()
                            getEvaluationLogs()
                        })
                };
                // Create a new button element
                const convertBtn = document.createElement('button');
                convertBtn.textContent = 'Convert TFJS';
                convertBtn.className = 'convert-button';
                convertBtn.onclick = function () {
                    fetch('/convert', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ model: newPath }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            alert('Success:', data);
                            console.log('Success:', data);
                        })
                        .catch((error) => {
                            alert('Error:', error);
                            console.error('Error:', error);
                        })
                };

                // Append the model and the button to the div
                div.appendChild(modelElement);
                div.appendChild(button);
                div.appendChild(convertBtn);

                // Append the div to the parent element
                parentElement.appendChild(div);
            } else if (item.endsWith('.txt') || item.endsWith('.json') || item.endsWith('.png') || item.endsWith('.jpg') || item.endsWith('.jpeg')) {
                // Create a new link element
                const linkElement = document.createElement('a');
                linkElement.href = `http://192.168.69.207:8080/${newPath.replace('models/', '')}`; // remove the initial "models/" part
                linkElement.textContent = item;
                linkElement.target = '_blank'; // open in a new tab
                linkElement.className = 'file-link';

                // Append the link to the parent element
                parentElement.appendChild(linkElement);
            }
        } else {
            // If the item is a folder
            const detailsElement = document.createElement('details');
            const summaryElement = document.createElement('summary');
            const tBtn = document.createElement('button');
            tBtn.textContent = 'Start Tensorboard';
            tBtn.addEventListener('click', () => {
                fetch('/start_tensorboard', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ logdir: newPath })
                })
                    .then(response => response.json())
                    .then(data => {
                        alert('Success', data);
                        console.log('Success:', data);
                    })
                    .catch((error) => {
                        alert('Error', error);
                        console.error('Error:', error);
                    }).finally(() => {
                        listProcesses()
                    })
            })
            summaryElement.textContent = item;
            detailsElement.appendChild(summaryElement);
            if (item == 'logs') {
                detailsElement.appendChild(tBtn);
            }
            createSubItems(node[item], detailsElement, newPath);
            parentElement.appendChild(detailsElement);
        }
    }
}

// Function to list the running processes
function listProcesses() {
    fetch(mlserver_url + '/processes', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // Create a table with a row for each process
            let table = '<table><tr><th>Name</th><th>PID</th><th>Start Time</th><th>Running Time</th><th>Command</th><th>Action</th></tr>';
            for (const process of data) {
                table += `
                    <tr>
                        <td>${process.name}</td>
                        <td>${process.pid}</td>
                        <td>${new Date(process.start_time * 1000).toLocaleString()}</td>
                        <td>${Math.floor(process.running_time / 3600)}h ${Math.floor(process.running_time / 60) % 60}m ${Math.floor(process.running_time % 60)}s</td>
                        <td>${process.cmdline}</td>
                        <td><button onclick="stopProcess('${process.pid}')">Stop</button></td>
                    </tr>
                `;
            }
            table += '</table>';

            // Add the table to the page
            document.getElementById('processes').innerHTML = table;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Function to stop a specific process
function stopProcess(process_id) {
    fetch(mlserver_url + '/stop_process/' + process_id, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message)
            console.log(data.message);
        })
        .catch((error) => {
            alert('Error:', error)
            console.error('Error:', error);
        }).finally(listProcesses)
}

