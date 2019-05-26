function resetForm() {
    $("input#word").val("");
    $(".add-form").remove();
}

function getDefaults() {
    if (null !== window.localStorage.getItem("language")) {
        return {
            language: window.localStorage.getItem("language"),
            deck: window.localStorage.getItem("deck")
        }
    }
    return false;
}


function setDefaults(language, deck) {
    window.localStorage.setItem("language", language);
    window.localStorage.setItem("deck", deck);
}

function populateDefaults() {
    const defaults = getDefaults();
    if (defaults) {
        $("select#decks").val(defaults.deck);
        $("select#language").val(defaults.language);
    }
}

function search() {
    $(".add-form").remove();
    const word_query = $("input#word").val();
    const deck_name = $("select#decks").val();
    const language = $("select#language").val();
    setDefaults(language, deck_name);
    $(".search-spinner").removeClass("d-none");
    $.get("/search",
        {
            word_query: word_query,
            deck_name: deck_name,
            language: language
        },
        function (data) {
            $(".container").append(data);
            $(".search-spinner").addClass("d-none");
        }
    );
    searchImages(word_query);
}

var pageNumber = 0;

function searchImages(query, loadMore) {
    if (!query) {
        $(".image-search-spinner").removeClass("d-none");
        query = $("input#image_query").val();
    }
    $.get("/search-images",
        {
            word_query: query,
            page: pageNumber
        },
        function (data) {
            if (!loadMore) {
                $(".gallery").html("");
                pageNumber = 0;
            }
            pageNumber++;
            $(".load-more").remove();
            $(".image-search-spinner").addClass("d-none");
            $("<button/>")
                .text("Load more images")
                .attr("type", "button")
                .addClass("load-more btn btn-link")
                .on("click", searchImages.bind(this, null, true))
                .appendTo(".gallery");
            data.forEach(function (link) {
                $("<img/>").attr("src", link).addClass("img-thumbnail").insertBefore(".load-more");
            });
            waitForSelectedGallery();
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
    const searchFormData = $(".search-form").serializeArray().reduce(function (obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    const addFormData = $(".add-form").serializeArray().reduce(function (obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    const formData = $.extend(searchFormData, addFormData);
    const selectedImages = $.map($(".img-selected"), function (el) {
        return $(el).attr("src");
    });
    formData["image_paths"] = JSON.stringify(selectedImages);
    formData["audio_filename"] = $(".btn-audio").data("audio");
    delete formData["image_query"];

    $.post("/add", formData, function (data) {
        $(".add-spinner").addClass("d-none");
        $(".add-form").remove();
        $("input#word").val("").focus();
        $(".alert-success").slideDown();
        setTimeout(function () {
            $(".alert-success").slideUp();
        }, 2000);
    });
}

function imgSelectWatch() {
    var selectedImages = [];
    $("body").on("click", ".gallery img", function () {
        $(this).addClass("img-selected");
        selectedImages.push(this.src);
        $(this).detach().appendTo(".gallery-selected");
    })
        .on("click", ".gallery-selected img", function () {
            $(this).removeClass("img-selected");
            selectedImages.pop(this.src);
            $(this).detach().insertBefore(".load-more");
        });
}

function enterWatch() {
    $("body").on("keypress", "input#word", function (e) {
        if (e.which === 13) {
            e.preventDefault();
            search();
        }
    })
        .on("keypress", "input#image_query", function (e) {
            if (e.which === 13) {
                e.preventDefault();
                searchImages();
            }
        });
}

function waitForSelectedGallery() {
    const sel = ".gallery-selected";
    let checkExist = setInterval(function () {
        if ($(sel).length) {
            clearInterval(checkExist);
            pasteWatch();
            dndWatch();
        }
    }, 100);
}

function pasteWatch() {
    const sel = ".gallery-selected";
    $(sel).pastableNonInputable()
        .off("pasteImage").on("pasteImage", function (e, data) {
        $("<img />")
            .attr("src", data.dataURL)
            .addClass("img-thumbnail img-selected")
            .appendTo(sel);
    });
}

function dndWatch() {
    const sel = ".gallery-selected";
    $(sel).off("dragover").on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
        e.originalEvent.dataTransfer.dropEffect = "copy";
        $(this).addClass("dnd-over");
    })
        .off("drop").on("drop", function(e) {
            e.stopPropagation();
            e.preventDefault();
            const files = e.originalEvent.dataTransfer.files; // Array of all files

            for (let i=0, file; file=files[i]; i++) {
                if (file.type.match(/image.*/)) {
                    const reader = new FileReader();

                    reader.onload = function(e2) {
                        // finished reading file data.
                        const img = $("<img />")
                            .attr("src", e2.target.result)
                            .addClass("img-thumbnail img-selected")
                            .appendTo(sel);
                    };

                    reader.readAsDataURL(file); // start reading the file data.
                }
            }
        });
}

$(document).ready(function () {
    populateDefaults();
    imgSelectWatch();
    enterWatch();
});