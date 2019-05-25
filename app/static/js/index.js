function resetForm() {
    $("input#word").val("");
    $(".add-form").remove();
}

function search() {
    $(".add-form").remove();
    const word_query = $("input#word").val();
    const deck_name = $("input#decks").val();
    $(".search-spinner").removeClass("d-none");
    $.get("/search",
        {
            word_query: word_query,
            deck_name: deck_name
        },
        function (data) {
            $(".container").append(data);
            $(".search-spinner").addClass("d-none");
        }
    );
    searchImages(word_query);
}

function searchImages(query) {
    if (!query) {
        $(".image-search-spinner").removeClass("d-none");
        query = $("input#image_query").val();
    }
    $.get("/search-images",
        {word_query: query},
        function(data) {
            $(".image-search-spinner").addClass("d-none");
            $(".gallery").html("");
            data.forEach(function (link) {
               $("<img/>").attr("src", link).addClass("img-thumbnail").appendTo(".gallery");
            });
        }
    );
}

function playSound(el) {
    const filename = $(el).data("audio");
    const audio = new Audio(filename);
    audio.play();
}

function add() {
    $(".add-spinner").removeClass("d-none");
    var searchFormData = $(".search-form").serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    var addFormData = $(".add-form").serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    const formData = $.extend(searchFormData, addFormData);
    const selectedImages = $.map($(".img-selected"), function(el) {
        return $(el).attr("src");
    });
    formData["image_paths"] = JSON.stringify(selectedImages);
    formData["audio_filename"] = $(".btn-audio").data("audio");
    delete formData["image_query"];

    $.post("/add", formData, function(data) {
        $(".add-spinner").addClass("d-none");
        $(".add-form").remove();
        $("input#word").val("").focus();
        $(".alert-success").removeClass("d-none");
        setTimeout(function() {
            $(".alert-success").addClass("d-none");
        }, 2000);
    });
}

function imgWatch() {
    var selectedImages = [];
    $("body").on("click", ".gallery img", function() {
        $(this).addClass("img-selected");
        selectedImages.push(this.src);
        $(this).detach().appendTo(".gallery-selected");
    })
        .on("click", ".gallery-selected img", function() {
            $(this).removeClass("img-selected");
            selectedImages.pop(this.src);
            $(this).detach().appendTo(".gallery");
        });
}

function enterWatch() {
    $("body").on("keypress", "input#word", function(e) {
        if (e.which === 13) {
            e.preventDefault();
            search();
        }
    })
        .on("keypress", "input#image_query", function(e) {
            if (e.which === 13) {
                e.preventDefault();
                searchImages();
            }
        });
}

$(document).ready(function() {
   imgWatch();
   enterWatch();
});