def loss_distance(model, images, labels, minimum_list):
        loss = 0
        classify_loss = loss_function(model, images, labels)
        loss += classify_loss
        for minimum in minimum_list:
            loss += (distance_factor/len(minimum_list)
             *kernel_function(computedistance(minimum, model), distance_width))

        return loss