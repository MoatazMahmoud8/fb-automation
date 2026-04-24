"""
Integration bridge between simple automation and production system
Allows using simple script alongside full system
"""

from src.main import FacebookAutomation
from simple_automation import SimpleAutomation


class HybridAutomation:
    """Use simple automation or production system based on mode"""

    @staticmethod
    def run_simple():
        """Run simplified automation (Arabic posts)"""
        automation = SimpleAutomation()
        return automation.run()

    @staticmethod
    def run_production():
        """Run full production automation (English + Arabic)"""
        automation = FacebookAutomation()
        return automation.run()

    @staticmethod
    def run_test():
        """Test all connections"""
        automation = FacebookAutomation()
        return automation.test_all_connections()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "--simple":
            print("Running Simple Automation (Arabic)...")
            success = HybridAutomation.run_simple()

        elif mode == "--production":
            print("Running Production Automation (Full)...")
            success = HybridAutomation.run_production()

        elif mode == "--test":
            print("Testing Connections...")
            success = HybridAutomation.run_test()

        else:
            print("Usage:")
            print("  python hybrid.py --simple      # Simple Arabic automation")
            print("  python hybrid.py --production  # Full production system")
            print("  python hybrid.py --test        # Test connections")
            sys.exit(1)

        sys.exit(0 if success else 1)

    else:
        print("No mode specified. Use: --simple, --production, or --test")
        sys.exit(1)
