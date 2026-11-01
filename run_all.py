from pathlib import Path

from common.terminal_controller import execute_with_terminal


ROOT = Path(__file__).resolve().parent
TESTS = [
    (number, folder)
    for number, folder in [
        (1, "TC-01_Register_User"),
        (2, "TC-02_Login_Correct"),
        (3, "TC-03_Login_Incorrect"),
        (4, "TC-04_Logout_User"),
        (5, "TC-05_Existing_Email"),
        (6, "TC-06_Contact_Us"),
        (7, "TC-07_Verify_Test_Cases"),
        (8, "TC-08_All_Products"),
        (9, "TC-09_Search_Product"),
        (10, "TC-10_Home_Subscription"),
        (11, "TC-11_Cart_Subscription"),
        (12, "TC-12_Add_Products"),
        (13, "TC-13_Product_Quantity"),
        (14, "TC-14_Register_Checkout"),
        (15, "TC-15_Register_Before_Checkout"),
        (16, "TC-16_Login_Checkout"),
        (17, "TC-17_Remove_Products"),
        (18, "TC-18_Category_Products"),
        (19, "TC-19_Brand_Products"),
        (20, "TC-20_Search_Cart_Login"),
        (21, "TC-21_Product_Review"),
        (22, "TC-22_Recommended_Items"),
        (23, "TC-23_Address_Checkout"),
        (24, "TC-24_Download_Invoice"),
        (25, "TC-25_Scroll_Arrow"),
        (26, "TC-26_Scroll_Without_Arrow"),
    ]
]


def run_all():
    results = []
    for number, folder in TESTS:
        case_dir = ROOT / folder
        log_path = case_dir / "execution.log"
        case_dir.joinpath("terminal").mkdir(parents=True, exist_ok=True)
        print(f"\nExecuting TC-{number:02d} in {case_dir}")
        try:
            passed = execute_with_terminal(case_dir)
        except Exception as error:
            passed = False
            with log_path.open("a", encoding="utf-8") as log:
                log.write(f"\nController error: {error}\nFINAL RESULT: FAIL\n")
            print(f"Controller error: {error}")
        results.append((number, folder, passed))
        print(f"TC-{number:02d} {folder}: {'PASS' if passed else 'FAIL'}")

    passed_count = sum(result[2] for result in results)
    print(f"\nTotal: {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {len(results) - passed_count}")
    return 0 if passed_count == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(run_all())
