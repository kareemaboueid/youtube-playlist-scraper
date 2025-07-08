function copy_text(p_element) {
    const text = p_element.textContent;
    navigator.clipboard.writeText(text).then(() => {
        p_element.classList.remove("txt");
        p_element.classList.add("txt-copied");
    });
}

function save_to_file() {
    const course_name = document.querySelector(
        ".info_details p strong + a"
    ).textContent;

    const sanitized_course_name = course_name
        .replace(/[^a-zA-Z0-9]/g, "_")
        .replace(/_+/g, "_")
        .replace(/^_+|_+$/g, "")
        .toLowerCase()
        .replace(/_/g, "-");

    const output_path = `${sanitized_course_name}.txt`;

    const sections = document.querySelectorAll(".single_data_section");

    let text_content = "";

    const scraping_time = document
        .querySelector("#scraping_time")
        .textContent.trim();
    const length = document
        .querySelector(".info_details p:nth-child(3)")
        .textContent.trim();
    const course_title = document
        .querySelector(".info_details a")
        .textContent.trim()
        .replace(/\s+/g, " ");

    text_content += `Time: ${scraping_time}s\n`;
    text_content += `${length}\n`;
    text_content += `Course: ${course_title}\n`;
    text_content += `||||||||||||||||||||||||||||||||||||||\n\n`;

    sections.forEach(section => {
        const title = section
            .querySelector(".title p")
            .textContent.trim()
            .replace(/\n/g, " ")
            .replace(/\s+/g, " ");

        const duration = section
            .querySelector(".duration p")
            .textContent.trim();
        text_content += `${title}\n${duration.replace(" minutes", "")}\n\n`;
    });

    const blob = new Blob([text_content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = output_path;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
