
function openMenu() {
    document.getElementById("sideNav").style.width = "100%";
    document.getElementById("sideNavOpen").style.display = "none";
    document.getElementById("sideNavClose").style.display = "flex";
}
  
function closeMenu() {
    document.getElementById("sideNav").style.width = "0";
    document.getElementById("sideNavClose").style.display = "none";
    document.getElementById("sideNavOpen").style.display = "flex";
}
