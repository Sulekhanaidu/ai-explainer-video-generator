# Entry point for running pipeline
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter topic: ")
    
    from pipeline import run_pipeline
    run_pipeline(topic,True,True,10,True)
