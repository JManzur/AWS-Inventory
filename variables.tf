# AWS Region: North of Virginia
variable "aws_region" {
  type    = string
}

variable "aws_profile" {
  type    = string
}

variable "enable_event_rules" {
  type    = bool
  default = false
}

/* Tags Variables */
#Use: tags = merge(var.project-tags, { Name = "${var.resource-name-tag}-place-holder" }, )
variable "project-tags" {
  type = map(string)
  default = {
    service     = "AWS-Inventory",
    environment = "POC",
    DeployedBy  = "JManzur - https://jmanzur.com/"
  }
}

#Use: tags = { Name = "${var.name-prefix}-lambda" }
variable "name-prefix" {
  type    = string
  default = "AWS-Inventory"
}

variable "bucket_name" {
  type = string
}

variable "Roles_List" {
 type = list(string)
}