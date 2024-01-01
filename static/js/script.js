document.addEventListener('DOMContentLoaded', function () {
    function editRole(button) {
        var editPanel = button.parentNode.nextElementSibling;
        editPanel.style.display = 'block';
    }

    function saveRole(button) {
        var editPanel = button.parentNode;
        var permissions = editPanel.querySelectorAll('.permission-checkbox:checked');
        var permissionsArray = Array.from(permissions).map(checkbox => checkbox.value);
        console.log('Permissions selected:', permissionsArray);
        editPanel.style.display = 'none';
    }

    function editPost(button) {
        var editPanel = button.parentNode.nextElementSibling;
        editPanel.style.display = 'block';
    }

    function savePost(button) {
        var editPanel = button.parentNode;
        console.log('Post details saved');
        editPanel.style.display = 'none';
    }

    var editRoleButtons = document.querySelectorAll('.edit-button');
    var saveRoleButtons = document.querySelectorAll('.save-button');
    var editPostButtons = document.querySelectorAll('.edit-post-button');
    var savePostButtons = document.querySelectorAll('.save-post-button');

    editRoleButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            editRole(this);
        });
    });

    saveRoleButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            saveRole(this);
        });
    });

    editPostButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            editPost(this);
        });
    });

    savePostButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            savePost(this);
        });
    });

    var userChartData = {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
            label: 'User Signups',
            data: [20, 25, 18, 30, 15],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };

    var trafficChartData = {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
            label: 'Page Views',
            data: [500, 700, 600, 800, 900],
            fill: false,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            pointRadius: 5,
            pointBackgroundColor: 'rgba(255, 99, 132, 1)',
            pointBorderColor: 'rgba(255, 255, 255, 1)',
            pointHoverRadius: 8,
            pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
            pointHoverBorderColor: 'rgba(255, 255, 255, 1)'
        }]
    };

    var ctxUser = document.getElementById('userChart').getContext('2d');
    var userChart = new Chart(ctxUser, {
        type: 'bar',
        data: userChartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var ctxTraffic = document.getElementById('trafficChart').getContext('2d');
    var trafficChart = new Chart(ctxTraffic, {
        type: 'line',
        data: trafficChartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
