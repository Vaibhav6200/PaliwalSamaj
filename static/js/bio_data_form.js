const occupation = document.getElementById("occupation");
const job_fields = document.querySelectorAll(".job_field");
const business_fields = document.querySelectorAll(".business_field");
occupation.addEventListener("input",function(){
    
    if(occupation.value == "job"){
        business_fields.forEach((field)=>{
            if(!field.classList.contains("d-none")){
                field.classList.add("d-none");
            }
        });
        job_fields.forEach((field)=>{
            field.classList.remove("d-none");
        });
    }
    if(occupation.value == "business"){
        job_fields.forEach((field)=>{
            if(!field.classList.contains("d-none")){
                field.classList.add("d-none");
            }
        });
        business_fields.forEach((field)=>{
            field.classList.remove("d-none");
        });
    }
});

const qualification = document.getElementById("qualification");
const school_fields = document.querySelectorAll(".school_field");
const ugpg_fields = document.querySelectorAll(".ugpg_field");
qualification.addEventListener("input",function(){
    
    if(qualification.value == "school"){
        ugpg_fields.forEach((field)=>{
            if(!field.classList.contains("d-none")){
                field.classList.add("d-none");
            }
        });
        school_fields.forEach((field)=>{
            field.classList.remove("d-none");
        });
    }
    if(qualification.value == "graduate" || qualification.value == "undergraduate"){
        school_fields.forEach((field)=>{
            if(!field.classList.contains("d-none")){
                field.classList.add("d-none");
            }
        });
        ugpg_fields.forEach((field)=>{
            field.classList.remove("d-none");
        });
    }
});

// Preview Image JS Start
function setupImagePreview(inputId, previewImageId, removeButtonId, dummyImageSrc) {
    const imageInput = document.getElementById(inputId);
    const previewImage = document.getElementById(previewImageId);
    const removeImgBtn = document.getElementById(removeButtonId);

    if (!imageInput || !previewImage || !removeImgBtn) {
        console.error('One or more required elements are missing. Please check the IDs provided.');
        return;
    }

    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        
        if (file) {
            const fileExtension = file.name.split('.').pop().toLowerCase();
            
            if (fileExtension === 'pdf') {
                previewImage.src = 'assets/DummyPdf.png';
                removeImgBtn.classList.remove("d-none");
            } else {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    removeImgBtn.classList.remove("d-none");
                };
                reader.readAsDataURL(file);
            }
        }
    });

    removeImgBtn.addEventListener('click', function() {
        previewImage.src = dummyImageSrc;
        imageInput.value = '';
        removeImgBtn.classList.add("d-none");
    });
}
setupImagePreview('profileImage','previewImage','remove-img-btn','images/profile.png');

// Preview Image JS End