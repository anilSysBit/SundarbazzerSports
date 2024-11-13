
document.addEventListener('DOMContentLoaded', function() {
    const provinceSelect = document.getElementById('id_province');
    const districtSelect = document.getElementById('id_district');

    const districtValue = districtSelect.value;
    const municipalitySelect = document.getElementById('id_municipality');
    // const areaSelect = document.getElementById('id_area');
    const municipalityValue = municipalitySelect.value


    // Function to load districts based on province selection
    function loadDistricts(provinceId) {
        fetch(`/ajax/load_districts/?province_id=${provinceId}`)
            .then(response => response.json())
            .then(data => {
                districtSelect.innerHTML = '<option value="">Select District</option>';
                data.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.id;
                    option.textContent = district.name;
                    districtSelect.appendChild(option);
                    if(option.value && option.value == districtValue){
                      option.selected = true
                    }
                    
                });
            });
    }

    // Function to load municipalities based on district selection
    function loadMunicipalities(districtId) {
        fetch(`/ajax/load_municipalities/?district_id=${districtId}`)
            .then(response => response.json())
            .then(data => {
                municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
                data.forEach(municipality => {
                    const option = document.createElement('option');
                    option.value = municipality.id;
                    option.textContent = municipality.name;
                    municipalitySelect.appendChild(option);
                    if(option.value && option.value == municipalityValue){
                      option.selected = true
                    }
                });
            });
    }

    // Function to load areas based on municipality selection
    // function loadAreas(municipalityId) {
    //     fetch(`/ajax/load_areas/?municipality_id=${municipalityId}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             areaSelect.innerHTML = '<option value="">Select Area</option>';
    //             data.forEach(area => {
    //                 const option = document.createElement('option');
    //                 option.value = area.id;
    //                 option.textContent = area.name;
    //                 areaSelect.appendChild(option);
    //             });
    //         });
    // }

    // Event listener for province selection
    provinceSelect.addEventListener('change', function() {
        const provinceId = this.value;
        if (provinceId) {
            loadDistricts(provinceId);
        } else {
            districtSelect.innerHTML = '<option value="">Select District</option>';
            municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
            areaSelect.innerHTML = '<option value="">Select Area</option>';
        }
    });

    // Event listener for district selection
    districtSelect.addEventListener('change', function() {
        const districtId = this.value;
        if (districtId) {
            loadMunicipalities(districtId);
        } else {
            municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
            areaSelect.innerHTML = '<option value="">Select Area</option>';
        }
    });

    // Event listener for municipality selection
    municipalitySelect.addEventListener('change', function() {
        const municipalityId = this.value;
        if (municipalityId) {
            loadAreas(municipalityId);
        } else {
            areaSelect.innerHTML = '<option value="">Select Area</option>';
        }
    });

    // Pre-populate the fields if editing
    if (provinceSelect.value) {
        loadDistricts(provinceSelect.value);
    }
    if (districtSelect.value) {
        loadMunicipalities(districtSelect.value);
    }
    if (municipalitySelect.value) {
        loadAreas(municipalitySelect.value);
    }
});

