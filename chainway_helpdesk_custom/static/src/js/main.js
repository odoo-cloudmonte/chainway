import { rpc } from "@web/core/network/rpc";

function showPopup(count) {
    if (count > 0) {
        const popup = document.createElement("div");

        popup.innerHTML = `⚠ You have ${count} overdue ticket(s)`;
        popup.style.position = "fixed";
        popup.style.top = "20px";
        popup.style.right = "20px";
        popup.style.background = "#FEF2F2";
        popup.style.border = "1px solid #FCA5A5";
        popup.style.padding = "12px 16px";
        popup.style.borderRadius = "10px";
        popup.style.zIndex = "99999";
        popup.style.color = "#991B1B";
        popup.style.boxShadow = "0 4px 20px rgba(0,0,0,0.15)";

        document.body.appendChild(popup);

        setTimeout(() => popup.remove(), 5000);
    }
}

export async function checkTickets() {
    const count = await rpc("/web/dataset/call_kw", {
        model: "ticket.helpdesk",
        method: "search_count",
        args: [[["is_overdue", "=", true]]],
        kwargs: {},
    });

    showPopup(count);
}

