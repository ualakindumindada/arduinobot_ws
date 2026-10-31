import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter


class SimpleParameter(Node):

    def __init__(self):
        super().__init__('simple_parameter')

        self.declare_parameter('simple_int_param', 28)
        self.declare_parameter('simple_string_param', 'Lakindu')

        self.add_on_set_parameters_callback(
            self.paramChangeCallback
        )

    def paramChangeCallback(self, params):
        result = SetParametersResult()
        result.successful = True

        for param in params:

            if param.name == 'simple_int_param':
                if param.type_ == Parameter.Type.INTEGER:
                    self.get_logger().info(
                        f'Parameter simple_int_param changed. '
                        f'New value is: {param.value}'
                    )
                else:
                    result.successful = False
                    result.reason = 'simple_int_param must be an integer'
                    return result

            elif param.name == 'simple_string_param':
                if param.type_ == Parameter.Type.STRING:
                    self.get_logger().info(
                        f'Parameter simple_string_param changed. '
                        f'New value is: {param.value}'
                    )
                else:
                    result.successful = False
                    result.reason = 'simple_string_param must be a string'
                    return result

        return result


def main(args=None):
    rclpy.init(args=args)

    simple_parameter = SimpleParameter()

    try:
        rclpy.spin(simple_parameter)
    except KeyboardInterrupt:
        pass
    finally:
        simple_parameter.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()