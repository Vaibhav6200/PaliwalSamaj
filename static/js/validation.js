// Bio Data Form Start

$(document).ready(function () {

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

  // Custom method: Birth time must not be future today
  $.validator.addMethod("birthTimeCheck", function (value, element) {
    const date = new Date($('#date_of_birth').val());
    const today = new Date();
    const inputTime = value;
    
    if (!value || !date || isNaN(date)) return false;

    const [hours, minutes] = inputTime.split(":");
    date.setHours(hours);
    date.setMinutes(minutes);

    return date <= today;
  }, "Birth time cannot be in the future");

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

  $("#contact-form").validate({
  rules: {
    name: {
      required: true,
      noSpace: true
    },
    father_name: {
      required: true,
      noSpace: true
    },
    mother_name: {
      required: true,
      noSpace: true
    },
    date_of_birth: {
      required: true,
      birthDateCheck: true
    },
    birth_place: {
      required: true,
      birthDateCheck: true
    },
    birth_time: {
      required: true,
      birthTimeCheck: true
    },
    gender: "required",
    marital_status: "required",
    height: {
      required: true,
      number: true,
      validHeight: true
    },
    phone_number: {
      required: true,
      tenDigits: true
    },
    whatsapp_number: {
      required: true,
      tenDigits: true
    },
    email: {
      required: true,
      emailFormat: true
    },
    gotra: {
      required: true,
      noSpace: true
    },
    address: {
      required: true,
      noSpace: true,
      addressClean: true
    },
    qualification: "required",
    occupation: "required",
    "12th_result": {
      required: function () {
        return $("#qualification").val() === "school";
      }
    },
    "12th_school_name": {
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
    name: { required: "Please enter your name" },
    father_name: { required: "Please enter your father's name" },
    mother_name: { required: "Please enter your mother's name" },
    date_of_birth: { required: "Please enter your birth date" },
    birth_place: { required: "Please enter your birth place" },
    birth_time: { required: "Please enter your birth time" },
    gender: "Please select your gender",
    marital_status: "Please select your marital status",
    height: { required: "Please enter your height" },
    phone_number: { required: "Please enter your phone number" },
    whatsapp_number: { required: "Please enter your WhatsApp number" },
    email: { required: "Please enter your email address" },
    gotra: { required: "Please enter your gotra" },
    address: { required: "Please enter your address" },
    qualification: "Please select your qualification",
    occupation: "Please select your occupation",
    "12th_result": { required: "Please enter your 12th result" },
    "12th_school_name": { required: "Please enter your 12th school name" },
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

// Shandesh Form Start
$("#sandeshForm").validate({
  rules: {
    contact: {
      required: true,
      emailOrPhone: true
    },
    subject: {
      required: true,
      validSubject: true
    },
    image: {
      required: true,
      imageSize: true
    },
    message: {
      required: true,
      validMessage: true
    }
  },
  messages: {
    contact: {
      required: "This field is required"
    },
    subject: {
      required: "This field is required"
    },
    image: {
      required: "Please upload an image"
    },
    message: {
      required: "This field is required"
    }
  },
  errorElement: "div",
  errorPlacement: function(error, element) {
    error.insertAfter(element);
  }
});
// Shandesh Form End