import java.util.Scanner;

public class LoginUI {
    public static void display() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Username: ");
        String username = scanner.nextLine();
        System.out.print("Password: ");
        String password = scanner.nextLine();

        String json = String.format("{\"username\":\"%s\", \"password\":\"%s\"}", username, password);

        try {
            String response = ApiClient.sendPostRequest("http://localhost:5000/login", json);
            if (response.contains("student")) {
                StudentDashboard.display(username);
            } else if (response.contains("admin")) {
                AdminDashboard.display(username);
            } else {
                System.out.println("Login failed.");
            }
        } catch (Exception e) {
            System.out.println("Error connecting to server: " + e.getMessage());
        }
    }
}
