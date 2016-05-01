//
//  ViewController.swift
//  SmartDoor
//
//  Created by Vaish Raman on 4/30/16.
//  Copyright © 2016 Vaish Raman. All rights reserved.
//

import UIKit

var imagePicker: UIImagePickerController!

class ViewController: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate {

    @IBOutlet var imageView: UIImageView!
    
    @IBAction func takePhoto(sender: UIButton) {
        imagePicker =  UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .Camera
        //displays image
        presentViewController(imagePicker, animated: true, completion: nil)
        //sends image to database
        
        let url = NSURL(string: "http://localhost:3000/picture")
        let request = NSURLRequest(URL: url!)

    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : AnyObject]) {
        imagePicker.dismissViewControllerAnimated(true, completion: nil)
        imageView.image = info[UIImagePickerControllerOriginalImage] as? UIImage
    }

}

