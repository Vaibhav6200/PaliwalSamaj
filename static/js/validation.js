// Bio Data Form Start

$(document).ready(function () {
  $('.only_alphabets').on('keypress', function (e) {
  var key = e.which;
  if (
    (key >= 65 && key <= 90) ||  // A–Z
    (key >= 97 && key <= 122) || // a–z
    key === 8 || key === 32      // Backspace or Space (optional)
  ) {
    return true;
  }
  return false;
});
   $.validator.addMethod("emailOrPhone", function(value) {
    return /^[^\s]+$/.test(value) && (/^\d{10}$/.test(value) || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
  }, "Enter a valid 10-digit number or email without spaces.");

  $.validator.addMethod("validSubject", function(value) {
    return /^[A-Za-z0-9]+(?:\s?[A-Za-z0-9]+)*$/.test(value.trim());
  }, "Subject must only contain letters and numbers.");

  $.validator.addMethod("validMessage", function(value) {
    return $.trim(value).length > 0 && value.length <= 2000;
  }, "Message is required and must be under 2000 characters.");

  $.validator.addMethod("imageSize", function(value, element) {
    if (element.files.length === 0) return false;
    return element.files[0].size <= 10485760;
  }, "Image is required and must be less than 10MB.");

  // Custom method: No leading or trailing spaces
  $.validator.addMethod("noSpace", function (value) {
    return value.trim() === value;
  }, "No leading or trailing spaces allowed");

  // Custom method: Birth date must not be future
  $.validator.addMethod("birthDateCheck", function (value) {
    const inputDate = new Date(value);
    const now = new Date();
    return inputDate <= now;
  }, "Birth date cannot be in the future");

  // Custom method: Phone/Whatsapp number must be exactly 10 digits
  $.validator.addMethod("tenDigits", function (value) {
    return /^\d{10}$/.test(value);
  }, "Enter exactly 10 digits");

  // Custom method: Valid email
  $.validator.addMethod("emailFormat", function (value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }, "Enter a valid email");

  // Custom method: No unnecessary punctuation in address
  $.validator.addMethod("addressClean", function (value) {
    return /^[a-zA-Z0-9\s,.-/]+$/.test(value);
  }, "Avoid unnecessary punctuation");

  // Custom method: Height range
  $.validator.addMethod("validHeight", function (value) {
    return value >= 24 && value <= 300;
  }, "Height must be between 24 and 300 cm");

  // Add custom validator for image file size (max 200KB)
  $.validator.addMethod("filesize500kb", function(value, element) {
    if (element.files.length === 0) return true;
      if (element.files[0].size > 500 * 1024) {
          Swal.fire({
              icon: 'error',
              title: 'File Too Large',
              text: 'Image size must be less than 200 KB.',
          });
          return false;
      }
      return true;
  }, "");

$("#contact-form").validate({
  rules: {
    full_name: {
      required: true,
      noSpace: true
    },
    father_name: {
      required: true,
      noSpace: true
    },
    mother_name: {
      noSpace: true
    },
    date_of_birth:{
      required: true,
      birthDateCheck:true
    },
    birth_place:{
      noSpace: true
    },

    phone_number: {
      required: true,
      maxlength:10,
      minlength:10,
      min:0
    },
    whatsapp_number: {
      maxlength:10,
      minlength:10,
      min:0
    },
    address:{
        required:true,
        addressClean:true
    },
    profileImage:{
      filesize500kb:true,
    },
    city:{
      required:true,
      noSpace:true
    },
    state:{
      required:true,
      noSpace:true
    },
    village:{
      required:true,
      noSpace:true
    },
    "school_class": {
      required: function () {
        return $("#qualification").val() === "school";
      }
    },
    "school_name": {
      required: function () {
        return $("#qualification").val() === "school";
      },
      noSpace: true
    },
    collge_uni_name: {
      required: function () {
        return $("#qualification").val() !== "school";
      },
      noSpace: true
    },
    degree_name: {
      required: function () {
        return $("#qualification").val() !== "school";
      },
      noSpace: true
    },
    company_name: {
      required: function () {
        return $("#occupation").val() === "job";
      },
      noSpace: true
    },
    job_location: {
      required: function () {
        return $("#occupation").val() === "job";
      },
      noSpace: true
    },
    job_description: {
      required: function () {
        return $("#occupation").val() === "job";
      }
    },
    business_name: {
      required: function () {
        return $("#occupation").val() === "business";
      },
      noSpace: true
    },
    business_location: {
      required: function () {
        return $("#occupation").val() === "business";
      },
      noSpace: true
    },
    business_description: {
      required: function () {
        return $("#occupation").val() === "business";
      }
    }
  },
  messages: {
    full_name: { required: "Please enter your full name" },
    father_name: { required: "Please enter your father's name" },
    date_of_birth: { required: "Please enter your birth date" },
    phone_number: { required: "Please enter your phone number" },
    address: { required: "Please enter your address" },
    city:{ required: "Please enter your city" },
    state:{ required: "Please enter your state" },
    village:{ required: "Please enter your village name" },
    "school_class": { required: "Please enter your 12th result" },
    "school_name": { required: "Please enter your 12th school name" },
    collge_uni_name: { required: "Please enter your college/university name" },
    degree_name: { required: "Please enter your degree name" },
    company_name: { required: "Please enter your company name" },
    job_location: { required: "Please enter your job location" },
    job_description: { required: "Please enter your job description" },
    business_name: { required: "Please enter your business name" },
    business_location: { required: "Please enter your business location" },
    business_description: { required: "Please enter your business description" }
  }
});


  // Show/Hide conditional fields
  $('#qualification').change(function () {
    const val = $(this).val();
    if (val === 'school') {
      $('.school_field').removeClass('d-none');
      $('.ugpg_field').addClass('d-none');
    } else {
      $('.ugpg_field').removeClass('d-none');
      $('.school_field').addClass('d-none');
    }
  });

  $('#occupation').change(function () {
    const val = $(this).val();
    if (val === 'job') {
      $('.job_field').removeClass('d-none');
      $('.business_field').addClass('d-none');
    } else if (val === 'business') {
      $('.business_field').removeClass('d-none');
      $('.job_field').addClass('d-none');
    } else {
      $('.job_field, .business_field').addClass('d-none');
    }
  });
});

// Bio Data Form End
$("#login-form").validate({
  rules: {
    mobile_number:{
      required: true,
      tenDigits: true
    }
  },
  messages: {
    mobile_number: {
      required: "Mobile Nnumber is required",
    },
  },
  errorElement: "div",
  errorPlacement: function(error, element) {
    error.insertAfter(element);
  }
});
// Shandesh Form End

// Community Form Start
// Custom rule for conditional required
 $.validator.addMethod("requiredIfOtherFilled", function (value, element, param) {
    return value || $(param).val() === "";
 }, "Please Enter both Start and Ending Pointing.");
//
//  // Custom rule to check age range logic
  $.validator.addMethod("ageRangeCheck", function () {
    let start = parseInt($("#startAge").val(), 10);
    let end = parseInt($("#endAge").val(), 10);
    if (!isNaN(start) && !isNaN(end)) {
      return start < end;
    }
    return true;
  }, "Start Age must be less than End Age");
//$("#search_family_form").validate({
//    rules: {
//      gender: {
//         required: true,
//      },
//      name: {
//         required: true,
//         noSpace:true,
//         maxLength:50
//      },
//
//    },
//    messages: {
//      gender: {
//        required: "Please Select the Gender",
//      },
//      name: {
//        required: "Please Enter the Name",
//        maxLength:"Please Enter Less than 50 Character."
//      },
//      family_search:{
//        required:"Please Enter email or phone number."
//      }
//    }
//  });
// Community Form End