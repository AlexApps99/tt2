document.getElementById("remove_marker").onclick = () => {
  fetch(current_data.id.toString() + ".json", { method: "DELETE" }).then(r => location.reload());
};
